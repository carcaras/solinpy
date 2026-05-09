from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RPCConfig:
    """Configuração para o cliente RPC Solana."""
    cluster: str = "devnet"
    custom_endpoint: Optional[str] = None
    timeout: float = 10.0
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    retryable_http_codes: tuple[int, ...] = field(
        default_factory=lambda: (429, 500, 502, 503, 504)
    )
    retryable_rpc_codes: tuple[int, ...] = field(default_factory=lambda: (-32004, -32005))
    retries: Optional[int] = None
    backoff_factor: Optional[float] = None

    def __post_init__(self) -> None:
        if self.retries is not None:
            self.max_retries = self.retries
        else:
            self.retries = self.max_retries

        if self.backoff_factor is not None:
            self.base_delay = self.backoff_factor
        else:
            self.backoff_factor = self.base_delay

@dataclass
class TokenBalance:
    mint: str
    amount: float
    decimals: int
    ui_amount: str
