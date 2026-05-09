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
            "sendTransaction",
            [tx_base64, {
                "encoding": "base64",
                "maxRetries": max_retries
            }])
        return resp["result"]
    
    def get_balance(self, address: str) -> int:
        """
        Returns the account balance in Lamports.
        
        Args:
            address: The base58-encoded public key of the account.
            
        Returns:
            int: The balance in Lamports.
        """
        resp = self._call("getBalance", [address])
        return resp["result"]["value"]

    def get_token_accounts_by_owner(self, address: str) -> list[Dict[str, Any]]:
        """
        Returns the list of SPL token accounts associated with an address.
        """
        TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
        
        sanitized_address = address.strip()
        
        params = [
            sanitized_address,
            {"programId": TOKEN_PROGRAM_ID},
            {"encoding": "jsonParsed", "commitment": "confirmed"} # Adicionado o commitment
        ]
        
        resp = self._call("getTokenAccountsByOwner", params)
        return resp["result"]["value"]
    
    def get_sol_balance(self, address: str) -> float:
        """
        Returns the account balance converted to SOL (user-friendly unit).

        Args:
            address: The base58-encoded public key of the account.

        Returns:
            float: The balance in SOL.
        """
        lamports = self.get_balance(address)
        # 1 SOL is equivalent to 1,000,000,000 Lamports
        return lamports / 1_000_000_000
    
    def get_token_balances(self, address: str) -> list[dict]:
        """
        Retrieves a simplified list of token balances for a given address.
        """
        raw_accounts = self.get_token_accounts_by_owner(address)
        balances = []
        
        for account in raw_accounts:
            info = account["account"]["data"]["parsed"]["info"]
            token_amount = info["tokenAmount"]
            
            balances.append({
                "mint": info["mint"],
                "amount": token_amount["uiAmount"],
                "decimals": token_amount["decimals"]
            })
            
        return balances
