import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from solders.pubkey import Pubkey

from solinpy.client.client import SolanaRPCClient
from solinpy.client.entities import RPCConfig
from solinpy.client.execptions import (
    RPCError,
    _format_context,
    _friendly_rpc_message,
)
from solinpy.utils.account_decoder import decode_account_data, decode_spl_token_account
from solinpy.wallet.mnemonic import _derive_slip10_ed25519, import_from_mnemonic


def _mock_urlopen_response(data: dict) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(data).encode()
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_rpc_config_post_init_with_aliases() -> None:
    cfg = RPCConfig(retries=7, backoff_factor=0.25)
    assert cfg.max_retries == 7
    assert cfg.base_delay == 0.25


def test_rpc_config_post_init_without_aliases() -> None:
    cfg = RPCConfig(max_retries=4, base_delay=0.5)
    assert cfg.retries == 4
    assert cfg.backoff_factor == 0.5


def test_format_context_empty_and_filtered() -> None:
    assert _format_context(None) == ""
    assert _format_context({"a": 1, "b": None}) == "a=1"


@pytest.mark.parametrize(
    ("code", "message", "expected"),
    [
        (-32601, "Method not found", "Metodo RPC desconhecido"),
        (-32000, "Account not found", "Conta invalida ou inexistente"),
        (-32000, "blockhash expired", "Blockhash expirado"),
        (-32004, "busy", "Servico RPC temporariamente indisponivel"),
        (None, "custom problem", "Erro RPC ao executar getX: custom problem"),
        (None, "", "Erro RPC ao executar getX."),
    ],
)
def test_friendly_rpc_message_variants(code: int | None, message: str, expected: str) -> None:
    msg = _friendly_rpc_message("getX", code, message)
    # Replace accents to keep assertion robust in mixed locales.
    normalized = (
        msg.replace("é", "e")
        .replace("á", "a")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("ê", "e")
    )
    assert expected in normalized


def test_rpc_error_str_without_details() -> None:
    err = RPCError("plain")
    assert str(err) == "plain"


def test_rpc_error_from_rpc_error_with_data() -> None:
    err = RPCError.from_rpc_error(
        "getX",
        {"code": "not-int", "message": "Method not found", "data": {"k": "v"}},
        context={"request_id": 1},
    )
    assert err.code is None
    assert err.context["request_id"] == 1
    assert err.context["rpc_data"] == {"k": "v"}


def test_rpc_error_from_transport_default_message() -> None:
    err = RPCError.from_transport_error("getX", RuntimeError("boom"))
    assert "Falha de comunicacao" in str(err).replace("ç", "c").replace("ã", "a")


def test_client_retryable_rpc_code_path() -> None:
    client = SolanaRPCClient(RPCConfig())
    assert client._is_retryable(None, rpc_error={"code": -32004}) is True


@patch("urllib.request.urlopen")
@patch("time.sleep")
def test_client_retries_rpc_error_then_succeeds(mock_sleep: MagicMock, mock_urlopen: MagicMock) -> None:
    mock_urlopen.side_effect = [
        _mock_urlopen_response({"error": {"code": -32004, "message": "temporarily unavailable"}}),
        _mock_urlopen_response({"result": "ok"}),
    ]
    client = SolanaRPCClient(RPCConfig(max_retries=1, base_delay=0.01, max_delay=0.01, timeout=1.0))
    assert client.get_health() == "ok"
    assert mock_sleep.call_count == 1


@patch("urllib.request.urlopen")
def test_client_http_non_retryable_raises_transport_error(mock_urlopen: MagicMock) -> None:
    mock_urlopen.side_effect = urllib.error.HTTPError("url", 400, "Bad Request", {}, MagicMock())
    client = SolanaRPCClient(RPCConfig(max_retries=0, timeout=1.0))
    with pytest.raises(RPCError) as exc:
        client.get_health()
    assert "Falha HTTP ao executar getHealth" in str(exc.value)


def test_client_balance_and_token_methods() -> None:
    client = SolanaRPCClient(RPCConfig())
    client._call = MagicMock(  # type: ignore[method-assign]
        side_effect=[
            {"result": {"value": 123}},
            {"result": {"value": [{"id": 1}]}},
        ]
    )

    balance = client.get_balance("  address  ")
    token_accounts = client.get_token_accounts_by_owner("  owner  ")

    assert balance == 123
    assert token_accounts == [{"id": 1}]

    first_call = client._call.call_args_list[0]
    assert first_call.args[0] == "getBalance"
    assert first_call.args[1] == ["address"]

    second_call = client._call.call_args_list[1]
    assert second_call.args[0] == "getTokenAccountsByOwner"
    assert second_call.args[1][0] == "owner"
    assert second_call.args[1][1]["programId"] == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"


def test_client_sol_and_token_balances_helpers() -> None:
    client = SolanaRPCClient(RPCConfig())
    client.get_balance = MagicMock(return_value=2_500_000_000)  # type: ignore[method-assign]
    assert client.get_sol_balance("x") == 2.5

    client.get_token_accounts_by_owner = MagicMock(  # type: ignore[method-assign]
        return_value=[
            {
                "account": {
                    "data": {
                        "parsed": {
                            "info": {
                                "mint": "Mint1",
                                "tokenAmount": {"uiAmount": 4.2, "decimals": 6},
                            }
                        }
                    }
                }
            }
        ]
    )
    assert client.get_token_balances("x") == [{"mint": "Mint1", "amount": 4.2, "decimals": 6}]


def test_mnemonic_import_from_mnemonic_success() -> None:
    phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    kp1 = import_from_mnemonic(phrase)
    kp2 = import_from_mnemonic(phrase)
    assert str(kp1.pubkey()) == str(kp2.pubkey())


def test_mnemonic_import_validation_errors() -> None:
    with pytest.raises(ValueError, match="Mnemonic must be a string"):
        import_from_mnemonic(123)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="Invalid mnemonic length"):
        import_from_mnemonic("too short")

    with pytest.raises(ValueError, match="Invalid mnemonic"):
        import_from_mnemonic(
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon invalid"
        )


def test_derive_slip10_ed25519_path_validation_and_output() -> None:
    seed = b"\x01" * 64

    with pytest.raises(ValueError, match="must start with 'm'"):
        _derive_slip10_ed25519(seed, "x/44'/501'/0'/0'")

    with pytest.raises(ValueError, match="requires hardened indices"):
        _derive_slip10_ed25519(seed, "m/44'/501'/0'/0")

    key = _derive_slip10_ed25519(seed, "m/44'/501'/0'/0'")
    assert isinstance(key, bytes)
    assert len(key) == 32


def test_decode_spl_token_account_all_optional_fields() -> None:
    mint = bytes(Pubkey.from_string("So11111111111111111111111111111111111111112"))
    owner = bytes(Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
    delegate = bytes(Pubkey.from_string("11111111111111111111111111111111"))
    close_authority = bytes(Pubkey.from_string("SysvarRent111111111111111111111111111111111"))

    data = bytearray()
    data.extend(mint)
    data.extend(owner)
    data.extend((25).to_bytes(8, "little"))
    data.append(1)  # has_delegate
    data.extend(delegate)
    data.append(7)  # unknown state
    data.append(1)  # is_native_option
    data.extend((999).to_bytes(8, "little"))
    data.extend((10).to_bytes(8, "little"))
    data.append(1)  # has_close_authority
    data.extend(close_authority)

    result = decode_spl_token_account(bytes(data))

    assert result["delegate"] is not None
    assert result["state"] == "unknown(7)"
    assert result["is_native"] is True
    assert result["native_amount"] == 999
    assert result["close_authority"] is not None


def test_decode_account_data_fallback_paths() -> None:
    unknown_type = decode_account_data(12345)
    assert unknown_type["program"] == "raw"
    assert unknown_type["encoding"] == "unknown"

    mint_fallback = decode_account_data(b"short", program_type="spl_token_mint")
    assert mint_fallback["program"] == "raw"
    assert mint_fallback["encoding"] == "bytes"
