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

import pytest

pytestmark = pytest.mark.integration

RUN_DEVNET_INTEGRATION = os.getenv("SOLINPY_RUN_DEVNET_INTEGRATION") == "1"
DEVNET_AIRDROP_LAMPORTS = int(os.getenv("SOLINPY_DEVNET_AIRDROP_LAMPORTS", "100000000"))
DEVNET_TRANSFER_LAMPORTS = int(os.getenv("SOLINPY_DEVNET_TRANSFER_LAMPORTS", "10000000"))
DEVNET_TIMEOUT = float(os.getenv("SOLINPY_DEVNET_TIMEOUT", "120"))
DEVNET_POLL_INTERVAL = float(os.getenv("SOLINPY_DEVNET_POLL_INTERVAL", "2"))
DEVNET_FUNDED_WALLET_PATH = Path(os.getenv("SOLINPY_DEVNET_FUNDED_WALLET_PATH", "my-wallet.json"))
DEVNET_REPORT_PATH = Path(
    os.getenv("SOLINPY_DEVNET_REPORT_PATH", "solinpy/tests/devnet_integration_report.md")
)

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
except ImportError:  # pragma: no cover - handled as a skipped integration module
    HAVE_SOLDERS = False
    Hash = Keypair = TransferParams = Transaction = None  # type: ignore[assignment]
    SolanaRPCClient = RPCConfig = request_airdrop = WalletManager = None  # type: ignore[assignment]


def _client() -> SolanaRPCClient:
    return SolanaRPCClient(RPCConfig(cluster="devnet", max_retries=3, timeout=15.0))


def _wait_for_signature_confirmation(
    client: SolanaRPCClient,
    signature: str,
    timeout: float = DEVNET_TIMEOUT,
    poll_interval: float = DEVNET_POLL_INTERVAL,
) -> None:
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
    client: SolanaRPCClient,
    signer: Keypair,
    receiver: Keypair,
    lamports: int,
    attempts: int = 3,
) -> str:
    last_error = None
    for _ in range(attempts):
        blockhash = Hash.from_string(client.get_latest_blockhash(commitment="finalized"))
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
    client: SolanaRPCClient,
    wallet: Keypair,
    expected_min_balance: int,
    timeout: float = DEVNET_TIMEOUT,
    poll_interval: float = DEVNET_POLL_INTERVAL,
) -> int:
    start = time.time()
    while time.time() - start < timeout:
        balance = client.get_balance(str(wallet.pubkey()))
        if balance >= expected_min_balance:
            return balance
        time.sleep(poll_interval)

    return client.get_balance(str(wallet.pubkey()))


def _fund_wallet(client: SolanaRPCClient, wallet: Keypair, lamports: int) -> dict:
    if DEVNET_FUNDED_WALLET_PATH.exists():
        funder = WalletManager.import_from_json(DEVNET_FUNDED_WALLET_PATH)
        funder_balance = client.get_balance(str(funder.pubkey()))
        if funder_balance < lamports:
            raise AssertionError(
                f"Funded wallet has insufficient balance. Required={lamports}, current={funder_balance}"
            )

        signature = _send_with_recent_blockhash(client, funder, wallet, lamports)
        funded_balance = _wait_for_min_balance(client, wallet, lamports)
        return {
            "signature": signature,
            "confirmed": funded_balance >= lamports,
            "source": "funded-wallet",
            "funder": str(funder.pubkey()),
            "funded_balance": funded_balance,
        }

    airdrop_result = request_airdrop(
        wallet,
        cluster="devnet",
        lamports=lamports,
        timeout=DEVNET_TIMEOUT,
        poll_interval=DEVNET_POLL_INTERVAL,
    )
    airdrop_result["source"] = "airdrop"
    return airdrop_result


@unittest.skipUnless(
    RUN_DEVNET_INTEGRATION and HAVE_SOLDERS,
    "Set SOLINPY_RUN_DEVNET_INTEGRATION=1 to run devnet integration tests.",
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
        wallet = WalletManager.generate_keypair()

        self.assertIsInstance(wallet, Keypair)
        self.assertEqual(len(bytes(wallet)), 64)
        self.assertTrue(str(wallet.pubkey()))

        self._append_report(
            "Carteira Gerada",
            [
                f"public_key: {wallet.pubkey()}",
                f"secret_key_bytes: {len(bytes(wallet))} bytes",
            ],
        )

    def test_devnet_airdrop_and_account_read(self) -> None:
        wallet = Keypair()
        client = _client()

        funding_result = _fund_wallet(client, wallet, DEVNET_AIRDROP_LAMPORTS)

        self.assertTrue(funding_result["confirmed"])

        balance = _wait_for_min_balance(client, wallet, DEVNET_AIRDROP_LAMPORTS)
        sol_balance = client.get_sol_balance(str(wallet.pubkey()))

        self.assertGreaterEqual(balance, DEVNET_AIRDROP_LAMPORTS)
        self.assertAlmostEqual(sol_balance, balance / 1_000_000_000, places=12)

        self._append_report(
            "Funding e Leitura de Conta",
            [
                f"wallet: {wallet.pubkey()}",
                f"source: {funding_result['source']}",
                f"signature: {funding_result['signature']}",
                f"confirmed: {funding_result['confirmed']}",
                f"balance_lamports: {balance}",
                f"balance_sol: {sol_balance}",
            ],
        )

    def test_devnet_send_sol_between_wallets(self) -> None:
        sender = Keypair()
        receiver = Keypair()
        client = _client()

        funding_result = _fund_wallet(client, sender, DEVNET_AIRDROP_LAMPORTS)

        self.assertTrue(funding_result["confirmed"])

        sender_before = _wait_for_min_balance(client, sender, DEVNET_AIRDROP_LAMPORTS)
        receiver_before = client.get_balance(str(receiver.pubkey()))

        signature = _send_with_recent_blockhash(
            client,
            sender,
            receiver,
            DEVNET_TRANSFER_LAMPORTS,
        )

        expected_receiver_balance = receiver_before + DEVNET_TRANSFER_LAMPORTS
        receiver_after = _wait_for_min_balance(client, receiver, expected_receiver_balance)
        sender_after = client.get_balance(str(sender.pubkey()))

        self.assertGreaterEqual(receiver_after, expected_receiver_balance)
        self.assertLess(sender_after, sender_before)

        self._append_report(
            "Transferencia de SOL",
            [
                f"sender: {sender.pubkey()}",
                f"receiver: {receiver.pubkey()}",
                f"funding_source: {funding_result['source']}",
                f"signature: {signature}",
                f"sender_before: {sender_before}",
                f"sender_after: {sender_after}",
                f"receiver_before: {receiver_before}",
                f"receiver_after: {receiver_after}",
                f"transferred_lamports: {DEVNET_TRANSFER_LAMPORTS}",
            ],
        )
