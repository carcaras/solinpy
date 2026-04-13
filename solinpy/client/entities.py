from dataclasses import dataclass
from typing import Optional


@dataclass
class RPCConfig:
    cluster: str = "devnet"
    custom_endpoint: Optional[str] = None
    timeout: float = 10.0
    retries: int = 3
    backoff_factor: float = 0.5
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    retryable_http_codes: tuple = (429, 500, 502, 503, 504)
    retryable_rpc_codes: tuple = (-32004, -32005)
