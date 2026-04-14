
import json
import time
import base64
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Union
from solinpy.client.entities import RPCConfig, AccountInfo

class SolanaRPCClient:
    def __init__(self, config: Optional[RPCConfig] = None):
        self.cfg = config or RPCConfig()
        self.endpoint = self.cfg.custom_endpoint or self._resolve_cluster_url()
        self._request_id = 0

    def _resolve_cluster_url(self) -> str:
        urls = {
            "devnet": "https://api.devnet.solana.com",
            "testnet": "https://api.testnet.solana.com",
            "mainnet": "https://api.mainnet-beta.solana.com"
        }
        return urls.get(self.cfg.cluster, urls["devnet"])

    def _call(self, method: str, params: list = None) -> Dict[str, Any]:
        self._request_id += 1
        payload = {"jsonrpc": "2.0", "id": self._request_id, "method": method, "params": params or []}
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        for attempt in range(1, self.cfg.retries + 2):
            try:
                with urllib.request.urlopen(req, timeout=self.cfg.timeout) as resp:
                    body = json.loads(resp.read())
                    if "error" in body:
                        raise RuntimeError(f"RPC error: {body['error']}")
                    return body

            except RuntimeError:
                raise
            except Exception as e:
                if attempt > self.cfg.retries:
                    raise ConnectionError(f"RPC failed after {attempt} attempts: {e}")
                time.sleep(self.cfg.backoff_factor * attempt)

    def get_health(self) -> str:
        return self._call("getHealth")["result"]

    def get_latest_blockhash(self, commitment: str = "confirmed") -> str:
        resp = self._call("getLatestBlockhash", [{"commitment": commitment}])
        return resp["result"]["value"]["blockhash"]

    def send_transaction(self, tx_base64: str, max_retries: int = 5) -> str:
        resp = self._call(
            "sendTransaction",
            [tx_base64, {
                "encoding": "base64",
                "maxRetries": max_retries
            }])
        return resp["result"]

    def get_account_info(
        self,
        public_key: str,
        commitment: str = "confirmed",
        encoding: str = "base64"
    ) -> Optional[AccountInfo]:
        """
        Consulta dados de uma conta na blockchain Solana.
        
        Args:
            public_key: Endereço da conta a ser consultada
            commitment: Nível de confirmação ('processed', 'confirmed', 'finalized')
            encoding: Codificação dos dados ('base64', 'jsonParsed', 'base58', 'base64+zstd')
        
        Returns:
            AccountInfo com dados estruturados da conta, ou None se a conta não existir
            
        Raises:
            ValueError: Se o endereço da conta for inválido
        """
        resp = self._call(
            "getAccountInfo",
            [
                public_key,
                {
                    "encoding": encoding,
                    "commitment": commitment
                }
            ]
        )
        
        value = resp["result"]["value"]
        
        # Conta não existe ou foi fechada
        if value is None:
            return None
        
        # Processa os dados da conta
        raw_data = value.get("data")
        
        # Desserializa dados base64 para bytes quando possível
        decoded_data = self._decode_account_data(raw_data, encoding)
        
        return AccountInfo(
            lamports=value["lamports"],
            owner=value["owner"],
            data=decoded_data,
            executable=value["executable"],
            rent_epoch=value["rentEpoch"],
            public_key=public_key
        )

    def get_balance(
        self,
        public_key: str,
        commitment: str = "confirmed"
    ) -> int:
        """
        Consulta o saldo de uma conta em lamports.
        
        Args:
            public_key: Endereço da conta
            commitment: Nível de confirmação ('processed', 'confirmed', 'finalized')
            
        Returns:
            Saldo em lamports (1 SOL = 10^9 lamports)
        """
        resp = self._call(
            "getBalance",
            [public_key, {"commitment": commitment}]
        )
        return resp["result"]["value"]

    @staticmethod
    def _decode_account_data(
        raw_data: Any,
        encoding: str
    ) -> Union[bytes, str, Dict[str, Any]]:
        """
        Desserializa dados brutos de uma conta.
        
        Args:
            raw_data: Dados brutos da resposta RPC
            encoding: Codificação utilizada
            
        Returns:
            Dados decodificados (bytes para base64, dict para jsonParsed, str para base58)
        """
        if raw_data is None:
            return b""
        
        # Dados já parseados como JSON (ex: programas SPL Token, Metaplex)
        if isinstance(raw_data, dict):
            return raw_data
        
        # Dados codificados em base64 (formato: [base64_string, "base64"])
        if isinstance(raw_data, list) and len(raw_data) >= 1:
            data_str = raw_data[0]
            try:
                return base64.b64decode(data_str)
            except Exception:
                return data_str
        
        # Dados em base58 ou outros formatos de string
        if isinstance(raw_data, str):
            return raw_data
        
        # Fallback: retorna dados brutos
        return raw_data