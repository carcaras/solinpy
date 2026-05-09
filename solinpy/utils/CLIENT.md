# 📦 Busca de Dados de Conta On-Chain

Módulo para consultar e desserializar dados de qualquer conta da blockchain Solana.

## Visão Geral

Esta implementação fornece uma base para integrações avançadas, permitindo:
- Consultar dados brutos e estruturados de contas on-chain
- Desserializar automaticamente dados de programas conhecidos (SPL Token, System Program)
- Facilitar a integração com futuros módulos do projeto

## Componentes Principais

### 1. Modelo de Dados: `AccountInfo`

**Local:** `solinpy/client/entities.py`

Dataclass que estrutura os dados retornados pela blockchain:

```python
@dataclass
class AccountInfo:
    lamports: int                    # Saldo em lamports (1 SOL = 10^9 lamports)
    owner: str                       # Endereço do programa proprietário
    data: Union[bytes, str, dict]    # Dados da conta (desserializados quando possível)
    executable: bool                 # Indica se contém programa executável
    rent_epoch: int                  # Epoch para pagamento de rent
    public_key: str                  # Endereço da conta consultada
    
    @property
    def sol_balance(self) -> float:  # Propriedade conveniente para saldo em SOL
```

### 2. Métodos do Client RPC

**Local:** `solinpy/client/client.py`

#### `get_account_info(public_key, commitment, encoding)`

Consulta dados completos de qualquer conta na blockchain.

**Parâmetros:**
- `public_key` (str): Endereço da conta
- `commitment` (str): Nível de confirmação - `'processed'`, `'confirmed'`, `'finalized'`
- `encoding` (str): Formato de codificação - `'base64'`, `'jsonParsed'`, `'base58'`, `'base64+zstd'`

**Retorna:**
- `Optional[AccountInfo]`: Dados estruturados da conta, ou `None` se não existir

**Exemplo:**
```python
from solinpy.client.client import SolanaRPCClient
from solinpy.client.entities import RPCConfig

client = SolanaRPCClient(RPCConfig(cluster="devnet"))

# Dados brutos (base64 decodificado para bytes)
account = client.get_account_info("So11111111111111111111111111111111111111112")
if account:
    print(f"Saldo: {account.sol_balance} SOL")
    print(f"Owner: {account.owner}")
    print(f"Dados brutos: {account.data}")  # bytes

# Dados parseados pelo RPC (ideal para SPL Token, Metaplex, etc.)
account = client.get_account_info(
    "TokenAccount1111111111111111111111111111111",
    encoding="jsonParsed"
)
if account and isinstance(account.data, dict):
    print(f"Dados estruturados: {account.data}")
```

#### `get_balance(public_key, commitment)`

Consulta rápida do saldo de uma conta em lamports.

**Parâmetros:**
- `public_key` (str): Endereço da conta
- `commitment` (str): Nível de confirmação

**Retorna:**
- `int`: Saldo em lamports

**Exemplo:**
```python
balance = client.get_balance("UserWallet1111111111111111111111111111111")
print(f"Saldo: {balance} lamports ({balance / 1e9} SOL)")
```

### 3. Utilitários de Desserialização

**Local:** `solinpy/utils/account_decoder.py`

Módulo completo para decodificar dados brutos de contas em estruturas legíveis.

#### Funções Básicas

```python
# Codificação/decodificação Base64
decode_base64_to_bytes(data: str) -> bytes
decode_bytes_to_base64(data: bytes) -> str

# Parsing de tipos primitivos
parse_pubkey_from_bytes(data: bytes, offset: int = 0) -> Pubkey
parse_u64_from_bytes(data: bytes, offset: int = 0, little_endian: bool = True) -> int
parse_u32_from_bytes(data: bytes, offset: int = 0, little_endian: bool = True) -> int
parse_u8_from_bytes(data: bytes, offset: int = 0) -> int
```

#### Decoders Específicos

##### SPL Token Account (106 bytes)

```python
decode_spl_token_account(data: bytes) -> Dict[str, Any]
```

**Estrutura retornada:**
```python
{
    "program": "SPL Token",
    "mint": "So11111111111111111111111111111111111111112",
    "owner": "UserWallet1111111111111111111111111111111",
    "amount": 1000000000,
    "delegate": None,  # ou endereço do delegate
    "state": "initialized",  # uninitialized | initialized | frozen
    "is_native": False,
    "native_amount": 0,
    "delegated_amount": 0,
    "close_authority": None
}
```

##### SPL Token Mint (82 bytes)

```python
decode_spl_token_mint(data: bytes) -> Dict[str, Any]
```

**Estrutura retornada:**
```python
{
    "program": "SPL Token Mint",
    "mint_authority": "AuthorityAddress...",  # ou None
    "supply": 1000000000,
    "decimals": 9,
    "is_initialized": True,
    "freeze_authority": "AuthorityAddress..."  # ou None
}
```

#### Decoder Genérico com Auto-Detecção

```python
decode_account_data(
    data: Union[bytes, str, Dict],
    program_type: str = "auto"
) -> Dict[str, Any]
```

**Tipos de programa suportados:**
- `"auto"`: Detecta automaticamente baseado no tamanho dos dados
  - 106 bytes → SPL Token Account
  - 82 bytes → SPL Token Mint
  - Outro → Dados brutos (hex)
- `"spl_token"`: Força decodificação como SPL Token Account
- `"spl_token_mint"`: Força decodificação como SPL Token Mint
- `"system"`: System Program
- `"raw"`: Retorna dados brutos em hexadecimal

**Exemplo:**
```python
from solinpy.utils.account_decoder import decode_account_data

# Auto-detecção
decoded = decode_account_data(account.data)
print(f"Tipo detectado: {decoded['program']}")

# Forçar tipo específico
decoded = decode_account_data(account.data, program_type="spl_token")
print(f"Mint: {decoded['mint']}")
print(f"Amount: {decoded['amount']}")
```

### 4. Fluxo de Desserialização Automática

O `get_account_info` já integra com o decoder para desserialização automática:

```python
# Com encoding base64 (padrão)
account = client.get_account_info("TokenAccount...")
# account.data já vem como bytes decodificados

# Com encoding jsonParsed (dados já estruturados pelo RPC)
account = client.get_account_info("TokenAccount...", encoding="jsonParsed")
# account.data vem como dict com dados parseados

# Desserializar manualmente quando necessário
from solinpy.utils.account_decoder import decode_account_data
decoded = decode_account_data(account.data, program_type="auto")
```

## Exemplos de Uso Avançado

### 1. Consultar Saldo de Token SPL

```python
# Obter dados da conta token
account = client.get_account_info("TokenAccountAddress...")
if account:
    decoded = decode_account_data(account.data, program_type="spl_token")
    
    # Obter informações do mint
    mint_account = client.get_account_info(decoded["mint"])
    mint_data = decode_account_data(mint_account.data, program_type="spl_token_mint")
    
    # Calcular saldo com decimais corretos
    decimals = mint_data["decimals"]
    amount = decoded["amount"] / (10 ** decimals)
    
    print(f"Token: {decoded['mint']}")
    print(f"Saldo: {amount} tokens")
    print(f"Owner: {decoded['owner']}")
```

### 2. Verificar Se Conta É Programa Executável

```python
account = client.get_account_info("ProgramAddress...")
if account:
    if account.executable:
        print("Esta conta contém um programa executável")
    else:
        print("Conta de dados normal")
    
    print(f"Owner program: {account.owner}")
```

### 3. Monitorar Múltiplas Contas

```python
addresses = [
    "Account1...",
    "Account2...",
    "Account3..."
]

for addr in addresses:
    account = client.get_account_info(addr)
    if account:
        print(f"{addr}: {account.sol_balance} SOL")
    else:
        print(f"{addr}: Conta não existe")
```

## Estrutura de Arquivos

```
solinpy/
├── client/
│   ├── client.py              # SolanaRPCClient com get_account_info e get_balance
│   └── entities.py            # AccountInfo e RPCConfig
├── utils/
│   ├── __init__.py
│   ├── account_decoder.py     # Módulo completo de desserialização
│   └── CLIENT.md              # Esta documentação
└── tests/
    ├── test_account_decoder.py  # 28 testes do decoder
    └── ...
```

## Testes

### Executar testes do client:
```bash
python -m pytest solinpy/client/test_client.py -v
```

### Executar testes do decoder:
```bash
python -m pytest solinpy/tests/test_account_decoder.py -v
```

### Executar todos os testes relacionados:
```bash
python -m pytest solinpy/client/test_client.py solinpy/tests/test_account_decoder.py -v
```

**Status atual:** 39 testes passando ✅

## Notas Técnicas

### Codificações Suportadas

| Encoding | Uso | Formato de Retorno |
|----------|-----|-------------------|
| `base64` (padrão) | Dados brutos | `bytes` (decodificado automaticamente) |
| `jsonParsed` | Dados interpretados pelo RPC | `dict` (estrutura dependente do programa) |
| `base58` | Legacy | `str` |
| `base64+zstd` | Comprimido | `bytes` (pode precisar descompressão adicional) |

### Níveis de Commitment

| Commitment | Descrição | Velocidade | Segurança |
|------------|-----------|------------|-----------|
| `processed` | Incluída no bloco mais recente | Mais rápida | Menor |
| `confirmed` (padrão) | Confirmada por voto supermajority | Balanceada | Balanceada |
| `finalized` | Confirmada por 31 blocos | Mais lenta | Máxima |

### Limitações Conhecidas

1. **Desserialização automática**: Atualmente suporta apenas SPL Token e SPL Token Mint. Outros programas (Metaplex, Serum, etc.) retornam dados brutos.

2. **Dados jsonParsed**: A estrutura exata depende da implementação do RPC do Solana e pode variar entre programas.

3. **Tamanho de dados**: Contas muito grandes (>10MB) podem causar timeouts. Ajuste `timeout` no `RPCConfig` se necessário.

## Extensões Futuras

- [ ] Adicionar decoders para Metaplex NFT
- [ ] Suporte a Program Derived Addresses (PDAs)
- [ ] Cache de consultas de conta
- [ ] WebSocket para monitoramento em tempo real
- [ ] Suporte a contas comprimidas (State Compression)
