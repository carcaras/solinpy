
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from solinpy.client.entities import RPCConfig

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