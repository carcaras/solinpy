import json
import time
import random
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Tuple
from solinpy.client.entities import RPCConfig

from solinpy.client.execptions import RPCError


class SolanaRPCClient:
    def __init__(self, config: Optional[RPCConfig] = None):
        self.cfg = config or RPCConfig()
        self.endpoint = self.cfg.custom_endpoint or self._resolve_cluster_url()
        self._request_id = 0

    def _resolve_cluster_url(self) -> str:
        urls = {
            "devnet": "https://api.devnet.solana.com",
            "testnet": "https://api.testnet.solana.com",
            "mainnet": "https://api.mainnet-beta.solana.com",
        }
        return urls.get(self.cfg.cluster, urls["devnet"])

    def _calc_backoff(self, attempt: int) -> float:
        delay = min(self.cfg.base_delay * (2**attempt), self.cfg.max_delay)
        jitter = random.uniform(0, delay * 0.5)
        return delay + jitter

    def _is_retryable(self, exc: Exception, rpc_error: Optional[dict] = None) -> bool:
        if isinstance(exc, urllib.error.HTTPError):
            return exc.code in self.cfg.retryable_http_codes
        if isinstance(exc, (urllib.error.URLError, ConnectionError, OSError, TimeoutError)):
            return True
        if rpc_error and rpc_error.get("code") in self.cfg.retryable_rpc_codes:
            return True
        return False

    def _call(self, method: str, params: list = None) -> Dict[str, Any]:
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params or [],
        }
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )

        last_exc = None
        for attempt in range(self.cfg.max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.cfg.timeout) as resp:
                    body = json.loads(resp.read())
                    if "error" in body:
                        err = body["error"]
                        if self._is_retryable(None, rpc_error=err):
                            if attempt < self.cfg.max_retries:
                                time.sleep(self._calc_backoff(attempt))
                                continue
                        raise RPCError(f"RPC Error {err.get('code')}: {err.get('message')}")
                    return body

            except urllib.error.HTTPError as e:
                last_exc = e
                if self._is_retryable(e) and attempt < self.cfg.max_retries:
                    time.sleep(self._calc_backoff(attempt))
                    continue
                break
            except Exception as e:
                last_exc = e
                if not self._is_retryable(e) or attempt >= self.cfg.max_retries:
                    break
                time.sleep(self._calc_backoff(attempt))
        raise RPCError(
            f"Request failed after {self.cfg.max_retries + 1} attempts. Last: {last_exc}"
        ) from last_exc

    def get_health(self) -> str:
        return self._call("getHealth")["result"]

    def get_latest_blockhash(self, commitment: str = "confirmed") -> str:
        resp = self._call("getLatestBlockhash", [{"commitment": commitment}])
        return resp["result"]["value"]["blockhash"]

    def send_transaction(self, tx_base64: str, max_retries: int = 5) -> str:
        resp = self._call(
            "sendTransaction", [tx_base64, {"encoding": "base64", "maxRetries": max_retries}]
        )
        return resp["result"]
