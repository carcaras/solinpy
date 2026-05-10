"""Integration tests against Solana devnet.

These tests are opt-in because they perform real network operations and
consume faucet capacity on devnet.
"""

from __future__ import annotations

import base64
import os
import time
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Dict

# Configurações de ambiente para habilitar os testes
RUN_DEVNET_INTEGRATION = os.getenv("SOLINPY_RUN_DEVNET_INTEGRATION") == "1"
DEVNET_AIRDROP_LAMPORTS = int(os.getenv("SOLINPY_DEVNET_AIRDROP_LAMPORTS", "100000000"))
DEVNET_TRANSFER_LAMPORTS = int(os.getenv("SOLINPY_DEVNET_TRANSFER_LAMPORTS", "10000000"))
DEVNET_TIMEOUT = float(os.getenv("SOLINPY_DEVNET_TIMEOUT", "120"))
DEVNET_POLL_INTERVAL = float(os.getenv("SOLINPY_DEVNET_POLL_INTERVAL", "2"))
DEVNET_FUNDED_WALLET_PATH = Path(
    os.getenv("SOLINPY_DEVNET_FUNDED_WALLET_PATH", "my-wallet.json")
)
DEVNET_REPORT_PATH = Path(
    os.getenv("SOLINPY_DEVNET_REPORT_PATH", "solinpy/tests/devnet_integration_report.md")
)

# Bloco para o VS Code entender os tipos (limpa os sinalizadores amarelos)
if TYPE_CHECKING:
    from solders.hash import Hash
    from solders.keypair import Keypair
    from solders.system_program import TransferParams
    from solders.transaction import Transaction
    from solinpy.client.client import SolanaRPCClient
    from solinpy.client.entities import RPCConfig
    from solinpy.utils.airdrop import request_airdrop
    from solinpy.wallet.manager import WalletManager

# Bloco de importação real para execução
try:
    from solders.hash import Hash
    from solders.keypair import Keypair
    from solders.system_program import TransferParams, transfer
    from solders.transaction import Transaction

    from solinpy.client.client import SolanaRPCClient
    from solinpy.client.entities import RPCConfig
    from solinpy.utils.airdrop import request_airdrop
    from solinpy.wallet.manager import WalletManager
    HAVE_SOLDERS = True
except ImportError:
    HAVE_SOLDERS = False
    # TRUQUE MESTRE: Em vez de None, usamos uma classe vazia.
    # Assim o Pylance entende que é um "Tipo" e não uma variável.
    class _MockType: pass
    Hash = Keypair = TransferParams = Transaction = _MockType  # type: ignore
    SolanaRPCClient = RPCConfig = request_airdrop = WalletManager = _MockType  # type: ignore

def _client() -> 'SolanaRPCClient':
    """Cria uma instância do cliente para a Devnet."""
    return SolanaRPCClient(RPCConfig(cluster="devnet", max_retries=3, timeout=15.0))

def _wait_for_signature_confirmation(
    client: 'SolanaRPCClient',
    signature: str,
    timeout: float = DEVNET_TIMEOUT,
    poll_interval: float = DEVNET_POLL_INTERVAL,
) -> None:
    """Aguarda a confirmação da transação na rede."""
    start = time.time()
    while time.time() - start < timeout:
        resp = client._call("getSignatureStatuses", [[signature]])
        statuses = resp.get("result", {}).get("value", [])

        if statuses and statuses[0] is not None:
            status = statuses[0]
            if status.get("err") is None and status.get("confirmationStatus") in (
                "confirmed",
                "finalized",
            ):
                return
        time.sleep(poll_interval)
    raise TimeoutError(f"Signature {signature} was not confirmed within {timeout} seconds.")

def _send_with_recent_blockhash(
    client: 'SolanaRPCClient',
    signer: 'Keypair',
    receiver: 'Keypair',
    lamports: int,
    attempts: int = 3,
) -> str:
    """Envia SOL garantindo que o blockhash esteja atualizado."""
    last_error = None
    for _ in range(attempts):
        blockhash_str = client.get_latest_blockhash(commitment="finalized")
        blockhash = Hash.from_string(blockhash_str)
        instruction = transfer(
            TransferParams(
                from_pubkey=signer.pubkey(),
                to_pubkey=receiver.pubkey(),
                lamports=lamports,
            )
        )
        tx = Transaction.new_signed_with_payer([instruction], signer.pubkey(), [signer], blockhash)
        try:
            signature = client.send_transaction(base64.b64encode(bytes(tx)).decode())
            _wait_for_signature_confirmation(client, signature)
            return signature
        except Exception as exc:
            last_error = exc
            if "BlockhashNotFound" not in str(exc) and "blockhash" not in str(exc).lower():
                raise
            time.sleep(1)
    raise RuntimeError(f"Failed to send transaction after {attempts} attempts") from last_error

def _wait_for_min_balance(
    client: 'SolanaRPCClient',
    wallet: 'Keypair',
    expected_min_balance: int,
    timeout: float = DEVNET_TIMEOUT,
    poll_interval: float = DEVNET_POLL_INTERVAL,
) -> int:
    """Aguarda até que o saldo da conta atinja o valor esperado."""
    start = time.time()
    while time.time() - start < timeout:
        balance = client.get_balance(str(wallet.pubkey()))
        if balance >= expected_min_balance:
            return balance
        time.sleep(poll_interval)
    return client.get_balance(str(wallet.pubkey()))

def _fund_wallet(client: 'SolanaRPCClient', wallet: 'Keypair', lamports: int) -> dict:
    """Abstração para financiar a carteira via arquivo local ou Airdrop."""
    if DEVNET_FUNDED_WALLET_PATH.exists():
        funder = WalletManager.import_from_json(DEVNET_FUNDED_WALLET_PATH)
        signature = _send_with_recent_blockhash(client, funder, wallet, lamports)
        funded_balance = _wait_for_min_balance(client, wallet, lamports)
        return {
            "signature": signature,
            "confirmed": funded_balance >= lamports,
            "source": "funded-wallet",
            "funded_balance": funded_balance,
        }
    airdrop_result = request_airdrop(wallet, cluster="devnet", lamports=lamports)
    airdrop_result["source"] = "airdrop"
    return airdrop_result

@unittest.skipUnless(
    RUN_DEVNET_INTEGRATION and HAVE_SOLDERS,
    "Set SOLINPY_RUN_DEVNET_INTEGRATION=1 to run integration tests.",
)
class TestDevnetIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        DEVNET_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        DEVNET_REPORT_PATH.write_text("# Devnet Integration Report\n\n", encoding="utf-8")

    def _append_report(self, title: str, lines: list[str]) -> None:
        with DEVNET_REPORT_PATH.open("a", encoding="utf-8") as report_file:
            report_file.write(f"## {title}\n")
            for line in lines:
                report_file.write(f"- {line}\n")
            report_file.write("\n")

    def test_generate_wallet_returns_valid_keypair(self) -> None:
        """Testa se a geração de carteira do framework é compatível com solders."""
        wallet = WalletManager.generate_keypair()
        self.assertIsInstance(wallet, Keypair)
        self.assertEqual(len(bytes(wallet)), 64)
        self._append_report("Wallet Generation", [f"public_key: {wallet.pubkey()}"])

    def test_devnet_airdrop_and_account_read(self) -> None:
        """Testa o fluxo de financiamento e leitura de saldo real."""
        wallet = Keypair()
        client = _client()
        funding_result = _fund_wallet(client, wallet, DEVNET_AIRDROP_LAMPORTS)
        self.assertTrue(funding_result["confirmed"])
        balance = _wait_for_min_balance(client, wallet, DEVNET_AIRDROP_LAMPORTS)
        self.assertGreaterEqual(balance, DEVNET_AIRDROP_LAMPORTS)
        self._append_report("Funding and Read", [
            f"wallet: {wallet.pubkey()}", 
            f"signature: {funding_result['signature']}"
        ])

    def test_devnet_send_sol_between_wallets(self) -> None:
        """Testa uma transferência real de SOL entre duas carteiras novas."""
        sender = Keypair()
        receiver = Keypair()
        client = _client()
        _fund_wallet(client, sender, DEVNET_AIRDROP_LAMPORTS)
        signature = _send_with_recent_blockhash(client, sender, receiver, DEVNET_TRANSFER_LAMPORTS)
        self.assertTrue(signature)
        self._append_report("SOL Transfer", [f"signature: {signature}"])