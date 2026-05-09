import pytest
from unittest.mock import MagicMock, patch
from solders.keypair import Keypair

from solinpy.utils.airdrop import create_airdrop, request_airdrop


class TestRequestAirdrop:
    """Testes para a função request_airdrop."""

    def test_create_airdrop_devnet_success(self) -> None:
        """Testa solicitação via create_airdrop com sucesso."""
        keypair = Keypair()

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client

            mock_client._call.side_effect = [
                {"result": "fake_signature_create"},
                {"result": {"value": [{"confirmationStatus": "confirmed", "err": None}]}},
                {"result": {"value": 1_000_000_000}},
            ]

            result = create_airdrop(keypair, cluster="devnet")

            assert result["signature"] == "fake_signature_create"
            assert result["confirmed"] is True
            assert result["balance"] == 1_000_000_000

    def test_airdrop_devnet_success(self) -> None:
        """Testa solicitação de airdrop na devnet com sucesso."""
        keypair = Keypair()

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client

            mock_client._call.side_effect = [
                {"result": "fake_signature_123"},
                {"result": {"value": [{"confirmationStatus": "confirmed", "err": None}]}},
                {"result": {"value": 1_000_000_000}},
            ]

            result = request_airdrop(keypair, cluster="devnet")

            assert result["signature"] == "fake_signature_123"
            assert result["confirmed"] is True
            assert result["balance"] == 1_000_000_000

            mock_client._call.assert_any_call(
                "requestAirdrop", [str(keypair.pubkey()), 1_000_000_000]
            )

    def test_airdrop_testnet_success(self) -> None:
        """Testa solicitação de airdrop na testnet com sucesso."""
        keypair = Keypair()

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client

            mock_client._call.side_effect = [
                {"result": "fake_signature_456"},
                {"result": {"value": [{"confirmationStatus": "finalized", "err": None}]}},
                {"result": {"value": 2_000_000_000}},
            ]

            result = request_airdrop(keypair, cluster="testnet")

            assert result["signature"] == "fake_signature_456"
            assert result["confirmed"] is True
            assert result["balance"] == 2_000_000_000

    def test_airdrop_invalid_cluster(self) -> None:
        """Testa se ValueError é levantado para clusters inválidos."""
        keypair = Keypair()

        with pytest.raises(ValueError) as exc_info:
            request_airdrop(keypair, cluster="mainnet")

        assert "devnet" in str(exc_info.value)
        assert "testnet" in str(exc_info.value)

    def test_airdrop_custom_lamports(self) -> None:
        """Testa solicitação de airdrop com quantidade customizada de lamports."""
        keypair = Keypair()
        custom_lamports = 500_000_000

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client

            mock_client._call.side_effect = [
                {"result": "fake_signature_789"},
                {"result": {"value": [{"confirmationStatus": "confirmed", "err": None}]}},
                {"result": {"value": custom_lamports}},
            ]

            result = request_airdrop(keypair, cluster="devnet", lamports=custom_lamports)

            assert result["confirmed"] is True
            assert result["balance"] == custom_lamports

            mock_client._call.assert_any_call(
                "requestAirdrop", [str(keypair.pubkey()), custom_lamports]
            )

    def test_airdrop_timeout_error(self) -> None:
        """Testa se TimeoutError é levantado quando o airdrop não é confirmado."""
        keypair = Keypair()

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client

            mock_client._call.side_effect = [
                {"result": "fake_signature_timeout"},
                {"result": {"value": [None]}},
                {"result": {"value": [None]}},
                {"result": {"value": [None]}},
            ]

            with pytest.raises(TimeoutError) as exc_info:
                request_airdrop(
                    keypair,
                    cluster="devnet",
                    timeout=0.1,
                    poll_interval=0.05,
                )

            assert "não foi confirmado" in str(exc_info.value)

    def test_airdrop_polling_until_confirmed(self) -> None:
        """Testa que a função faz polling até o airdrop ser confirmado."""
        keypair = Keypair()
        call_count = 0

        def mock_call(method: str, params: list = None) -> dict:
            nonlocal call_count
            call_count += 1

            if method == "requestAirdrop":
                return {"result": "fake_signature_polling"}
            elif method == "getSignatureStatuses":
                if call_count < 4:
                    return {"result": {"value": [{"confirmationStatus": "processed"}]}}
                else:
                    return {"result": {"value": [{"confirmationStatus": "confirmed"}]}}
            elif method == "getBalance":
                return {"result": {"value": 1_000_000_000}}
            return {}

        with patch("solinpy.utils.airdrop.SolanaRPCClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client._call.side_effect = mock_call

            result = request_airdrop(keypair, cluster="devnet", timeout=5.0, poll_interval=0.05)

            assert result["confirmed"] is True
            assert call_count >= 4
