
from dataclasses import dataclass
from typing import Optional


@dataclass
class RPCConfig:
    cluster: str = "devnet"
    custom_endpoint: Optional[str] = None
    timeout: float = 10.0
    retries: int = 3
    backoff_factor: float = 0.5
