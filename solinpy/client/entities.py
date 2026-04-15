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
class AccountInfo:
    """
    Dados estruturados de uma conta on-chain.
    
    Attributes:
        lamports: Salda da conta em lamports (1 SOL = 10^9 lamports)
        owner: Endereço da conta proprietária (programa que gerencia esta conta)
        data: Dados brutos da conta (bytes ou string base64)
        executable: Indica se a conta contém um programa executável
        rent_epoch: Epoch em que a conta próxima pagará rent
        public_key: Endereço da conta consultada
    """
    lamports: int
    owner: str
    data: Union[bytes, str, Dict[str, Any]]
    executable: bool
    rent_epoch: int
    public_key: str
    
    @property
    def sol_balance(self) -> float:
        """Retorna o saldo em SOL (convertido de lamports)."""
        return self.lamports / 1_000_000_000
