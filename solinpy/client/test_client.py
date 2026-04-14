import unittest
from unittest.mock import patch, MagicMock
import json
import base64
import urllib.error
from .client import SolanaRPCClient, RPCConfig

class TestSolanaRPCClient(unittest.TestCase):
    def setUp(self):
        # retries=1 para testes rápidos (1 chamada inicial + 1 retry = 2 total)
        self.config = RPCConfig(cluster="devnet", retries=1, timeout=1.0)

    def _mock_urlopen_response(self, data: dict):
        """Helper para criar um mock compatível com context manager"""
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(data).encode()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    # 🟢 1. Resolução de endpoints
    def test_endpoint_resolution(self):
        c1 = SolanaRPCClient(RPCConfig(cluster="mainnet"))
        self.assertEqual(c1.endpoint, "https://api.mainnet-beta.solana.com")

        c2 = SolanaRPCClient(RPCConfig(custom_endpoint="https://meu-rpc.com"))
        self.assertEqual(c2.endpoint, "https://meu-rpc.com")

    # 🟢 2. Sucesso básico
    @patch("urllib.request.urlopen")
    def test_get_health_success(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({"result": "ok"})
        client = SolanaRPCClient(self.config)
        self.assertEqual(client.get_health(), "ok")

    @patch("urllib.request.urlopen")
    def test_get_latest_blockhash(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {"value": {"blockhash": "8xYz...abc"}}
        })
        client = SolanaRPCClient(self.config)
        self.assertEqual(client.get_latest_blockhash(), "8xYz...abc")

    # 🟡 3. Retry em falhas de rede
    @patch("urllib.request.urlopen")
    def test_retry_on_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("connection refused")
        client = SolanaRPCClient(self.config)
        with self.assertRaises(ConnectionError):
            client.get_health()
        # 1 tentativa inicial + 1 retry = 2 chamadas
        self.assertEqual(mock_urlopen.call_count, 2)

    # 🔴 4. Tratamento de erro RPC
    @patch("urllib.request.urlopen")
    def test_rpc_error_response(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "error": {"code": -32005, "message": "Blockhash expired"}
        })
        client = SolanaRPCClient(self.config)
        with self.assertRaises(RuntimeError) as ctx:
            client.get_health()
        self.assertIn("Blockhash expired", str(ctx.exception))

    # 🔵 5. Validação do payload de sendTransaction
    @patch("urllib.request.urlopen")
    def test_send_transaction_payload(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({"result": "5sig..."})
        client = SolanaRPCClient(self.config)
        sig = client.send_transaction("base64payload==")
        self.assertEqual(sig, "5sig...")

        # Verifica se o JSON-RPC foi montado corretamente
        call_args = mock_urlopen.call_args[0][0]
        payload = json.loads(call_args.data)
        self.assertEqual(payload["method"], "sendTransaction")
        self.assertEqual(payload["params"][0], "base64payload==")
        self.assertEqual(payload["params"][1]["encoding"], "base64")
        self.assertEqual(payload["params"][1]["maxRetries"], 5)

    # 🟢 6. get_account_info - conta existente
    @patch("urllib.request.urlopen")
    def test_get_account_info_success(self, mock_urlopen):
        # Simula resposta RPC para conta com dados base64
        account_data = base64.b64encode(b"test data").decode()
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {
                "value": {
                    "lamports": 1000000000,
                    "owner": "11111111111111111111111111111111",
                    "data": [account_data, "base64"],
                    "executable": False,
                    "rentEpoch": 0
                }
            }
        })
        client = SolanaRPCClient(self.config)
        account = client.get_account_info("So11111111111111111111111111111111111111112")
        
        self.assertIsNotNone(account)
        self.assertEqual(account.lamports, 1000000000)
        self.assertEqual(account.sol_balance, 1.0)
        self.assertEqual(account.owner, "11111111111111111111111111111111")
        self.assertEqual(account.data, b"test data")
        self.assertFalse(account.executable)
        self.assertEqual(account.public_key, "So11111111111111111111111111111111111111112")

    # 🟡 7. get_account_info - conta inexistente
    @patch("urllib.request.urlopen")
    def test_get_account_info_not_found(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {"value": None}
        })
        client = SolanaRPCClient(self.config)
        account = client.get_account_info("SomeAccount111111111111111111111111111111")
        
        self.assertIsNone(account)

    # 🟢 8. get_account_info - dados jsonParsed
    @patch("urllib.request.urlopen")
    def test_get_account_info_json_parsed(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {
                "value": {
                    "lamports": 2039280,
                    "owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    "data": {
                        "state": "initialized",
                        "mint": "So11111111111111111111111111111111111111112",
                        "owner": "UserAddress1111111111111111111111111111111"
                    },
                    "executable": False,
                    "rentEpoch": 100
                }
            }
        })
        client = SolanaRPCClient(self.config)
        account = client.get_account_info(
            "TokenAccount1111111111111111111111111111111",
            encoding="jsonParsed"
        )
        
        self.assertIsNotNone(account)
        self.assertEqual(account.lamports, 2039280)
        self.assertIsInstance(account.data, dict)
        self.assertEqual(account.data["state"], "initialized")

    # 🟢 9. get_balance
    @patch("urllib.request.urlopen")
    def test_get_balance(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {"value": 5000000000}
        })
        client = SolanaRPCClient(self.config)
        balance = client.get_balance("UserWallet1111111111111111111111111111111111")
        
        self.assertEqual(balance, 5000000000)

    # 🔵 10. Validação do payload de get_account_info
    @patch("urllib.request.urlopen")
    def test_get_account_info_payload(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_urlopen_response({
            "result": {"value": None}
        })
        client = SolanaRPCClient(self.config)
        client.get_account_info(
            "TestAccount111111111111111111111111111111111",
            commitment="finalized",
            encoding="base58"
        )
        
        # Verifica se o JSON-RPC foi montado corretamente
        call_args = mock_urlopen.call_args[0][0]
        payload = json.loads(call_args.data)
        self.assertEqual(payload["method"], "getAccountInfo")
        self.assertEqual(payload["params"][0], "TestAccount111111111111111111111111111111111")
        self.assertEqual(payload["params"][1]["commitment"], "finalized")
        self.assertEqual(payload["params"][1]["encoding"], "base58")

if __name__ == "__main__":
    unittest.main()