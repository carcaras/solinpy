# Solana RPC Client

Cliente JSON-RPC para interação com a blockchain Solana. Implementado com a biblioteca padrão do Python (`urllib`), sem dependências externas.

## Visão Geral

```
RPCConfig (dataclass)     → Configuração do cliente
SolanaRPCClient (classe)  → Cliente RPC com retry e tratamento de erros
```

## Configuração

### `RPCConfig`

Dataclass que define os parâmetros de conexão.

| Parâmetro | Tipo | Default | Descrição |
|---|---|---|---|
| `cluster` | `str` | `"devnet"` | Rede alvo: `"devnet"`, `"testnet"`, `"mainnet"` |
| `custom_endpoint` | `str \| None` | `None` | URL customizada (sobrepõe `cluster`) |
| `timeout` | `float` | `10.0` | Timeout por requisição (segundos) |
| `retries` | `int` | `3` | Número de retries em caso de erro de rede |
| `backoff_factor` | `float` | `0.5` | Multiplicador de espera entre retries |

```python
from solinpy.client.entities import RPCConfig

config = RPCConfig(
    cluster="mainnet",
    timeout=15.0,
    retries=5,
    backoff_factor=1.0
)
```

> **`retries`** funciona como: `1` tentativa inicial + `retries` tentativas extras. Exemplo: `retries=1` → até 2 chamadas no total.

## Uso

### Básico

```python
from solinpy.client.client import SolanaRPCClient
from solinpy.client.entities import RPCConfig

client = SolanaRPCClient(RPCConfig(cluster="devnet"))

# Verificar saúde do nó
status = client.get_health()  # → "ok"

# Obter blockhash recente
blockhash = client.get_latest_blockhash()  # → "8xYz...abc"

# Enviar transação
tx_id = client.send_transaction("base64encoded_tx")  # → "5sig..."
```

### Endpoint customizado

```python
client = SolanaRPCClient(
    RPCConfig(custom_endpoint="https://meu-rpc-helium.com")
)
```

## Referência da API

### `SolanaRPCClient`

#### `__init__(config: RPCConfig | None = None)`

Cria uma instância do cliente. Se `config` for omitido, usa defaults (`devnet`, timeout 10s, 3 retries).

#### `get_health() → str`

Chama o método `getHealth` do nó. Retorna `"ok"` se o nó estiver operacional.

**Exceções:**
- `RuntimeError` — o nó retornou um erro RPC
- `ConnectionError` — falha de rede após todos os retries

#### `get_latest_blockhash(commitment: str = "confirmed") → str`

Retorna o blockhash mais recente. O parâmetro `commitment` aceita `"processed"`, `"confirmed"` ou `"finalized"`.

#### `send_transaction(tx_base64: str, max_retries: int = 5) → str`

Envia uma transação codificada em base64. O `max_retries` é o parâmetro do protocolo Solana — quantas vezes o nó deve tentar reenviar a transação.

> **Atenção:** este `max_retries` é diferente do `retries` do `RPCConfig`. O primeiro é do protocolo Solana (lado do servidor), o segundo é do cliente (lado da rede).

**Retorna:** signature da transação (string).

## Resolução de Endpoints

| Cluster | URL |
|---|---|
| `devnet` | `https://api.devnet.solana.com` |
| `testnet` | `https://api.testnet.solana.com` |
| `mainnet` | `https://api.mainnet-beta.solana.com` |

Precedência: `custom_endpoint` > `cluster`

## Tratamento de Erros

O cliente diferencia dois tipos de erro:

| Tipo | Comportamento |
|---|---|
| **Erro RPC** (`RuntimeError`) | Propagado imediatamente — sem retry. Ex: "Blockhash expired" |
| **Erro de rede** (`ConnectionError`) | Aplica retry com backoff exponencial |

```python
try:
    client.get_health()
except RuntimeError as e:
    # Erro retornado pelo nó (ex: método inválido, parâmetros errados)
    print(f"Erro RPC: {e}")
except ConnectionError as e:
    # Falha de rede/timeout após todos os retries
    print(f"Rede: {e}")
```

## Backoff Exponencial

Entre cada retry, o cliente espera: `backoff_factor × attempt` segundos.

```
retries=3, backoff_factor=0.5

Tentativa 1  → erro → sleep 0.5s
Tentativa 2  → erro → sleep 1.0s
Tentativa 3  → erro → sleep 1.5s
Tentativa 4  → erro → ConnectionError
```

## Limitações Conhecidas

1. **Síncrono e bloqueante** — usa `urllib`, não suporta async nativamente
2. **Não é thread-safe** — `_request_id` é compartilhado e não protegido por lock
3. **Sem logger** — retries acontecem silenciosamente
4. **Sem validação de resposta** — se `"result"` estiver ausente, gera `KeyError`
5. **Dependência de `entities.py`** — `RPCConfig` foi movido para `solinpy.client.entities`

## Estrutura de Arquivos

```
solinpy/client/
├── client.py        # SolanaRPCClient
├── entities.py      # RPCConfig
└── test_client.py   # Testes unitários
```
