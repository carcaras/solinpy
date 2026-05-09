from dataclasses import dataclass
from typing import Optional, Dict, Any, Union


@dataclass
class RPCConfig:
    """Configuração para o cliente RPC Solana."""
    cluster: str = "devnet"
    custom_endpoint: Optional[str] = None
    timeout: float = 10.0
    retries: int = 3
    backoff_factor: float = 0.5

@dataclass
class TokenBalance:
    mint: str
    amount: float
    decimals: int
    ui_amount: str
