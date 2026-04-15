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
| `max_retries` | `int` | `3` | Número máximo de retries em caso de erro |
| `base_delay` | `float` | `1.0` | Delay base para backoff exponencial (segundos) |
| `max_delay` | `float` | `30.0` | Delay máximo entre retries (segundos) |
| `retryable_http_codes` | `tuple` | `(429, 500, 502, 503, 504)` | Códigos HTTP que disparam retry |
| `retryable_rpc_codes` | `tuple` | `(-32004, -32005)` | Códigos de erro RPC que disparam retry |

```python
from solinpy.client.entities import RPCConfig

config = RPCConfig(
    cluster="mainnet",
    timeout=15.0,
    max_retries=5,
    base_delay=1.0,
    max_delay=30.0
)
```

> **`max_retries`** define o número máximo de tentativas adicionais. Exemplo: `max_retries=2` → 1 tentativa inicial + 2 retries = 3 chamadas no total.

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
- `RPCError` — erro retornado pelo nó ou falha de rede após todos os retries

#### `get_latest_blockhash(commitment: str = "confirmed") → str`

Retorna o blockhash mais recente. O parâmetro `commitment` aceita `"processed"`, `"confirmed"` ou `"finalized"`.

#### `send_transaction(tx_base64: str, max_retries: int = 5) → str`

Envia uma transação codificada em base64. O `max_retries` é o parâmetro do protocolo Solana — quantas vezes o nó deve tentar reenviar a transação.

> **Atenção:** este `max_retries` é diferente do `max_retries` do `RPCConfig`. O primeiro é do protocolo Solana (lado do servidor), o segundo é do cliente (lado da rede).

**Retorna:** signature da transação (string).

## Resolução de Endpoints

| Cluster | URL |
|---|---|
| `devnet` | `https://api.devnet.solana.com` |
| `testnet` | `https://api.testnet.solana.com` |
| `mainnet` | `https://api.mainnet-beta.solana.com` |

Precedência: `custom_endpoint` > `cluster`

## Tratamento de Erros

Todas as exceções são encapsuladas em `RPCError`, que contém a causa original como chained exception.

| Tipo de Erro | Comportamento |
|---|---|
| **HTTP 429 / 5xx** | Retry com backoff exponencial (códigos em `retryable_http_codes`) |
| **Erro de rede** (`URLError`, `OSError`, `TimeoutError`) | Retry com backoff exponencial |
| **Erro RPC retryable** (códigos em `retryable_rpc_codes`) | Retry com backoff exponencial |
| **Erro RPC não-retryable** (ex: `-32600 Invalid Request`) | Propagado imediatamente — sem retry |

```python
from solinpy.client.execptions import RPCError

try:
    client.get_health()
except RPCError as e:
    # Pode ser erro de rede, HTTP ou RPC
    # A causa original está disponível como e.__cause__
    print(f"Erro: {e}")
```

### Códigos de Erro RPC

| Código | Significado | Retry? |
|---|---|---|
| `-32004` | Slot unavailable | Sim |
| `-32005` | Blockhash expired | Sim |
| `-32600` | Invalid Request | Não |
| `-32601` | Method not found | Não |
| `-32602` | Invalid params | Não |
| `-32603` | Internal error | Não |

## Backoff Exponencial com Jitter

Entre cada retry, o cliente espera: `min(base_delay × 2^attempt, max_delay) + jitter`, onde jitter é um valor aleatório entre 0 e 50% do delay calculado.

```
max_retries=2, base_delay=1.0, max_delay=30.0

Tentativa 0  → erro → sleep ~1.0s + jitter
Tentativa 1  → erro → sleep ~2.0s + jitter
Tentativa 2  → erro → RPCError
```

O jitter ajuda a evitar que múltiplos clientes sincronizem seus retries (thundering herd problem).

## Limitações Conhecidas

1. **Síncrono e bloqueante** — usa `urllib`, não suporta async nativamente
2. **Não é thread-safe** — `_request_id` é compartilhado e não protegido por lock
3. **Sem logger** — retries acontecem silenciosamente
4. **Sem validação de resposta** — se `"result"` estiver ausente, gera `KeyError`
5. **Dependência de `entities.py`** — `RPCConfig` está em `solinpy.client.entities`

## Executando os Testes

Os testes usam apenas a biblioteca padrão do Python (`unittest`). Nenhuma dependência extra é necessária.

### Todos os testes

```bash
python -m unittest solinpy.client.test_client -v
```

### Arquivo específico

```bash
python -m unittest solinpy.client.test_client.TestSolanaRPCClient -v
python -m unittest solinpy.client.test_client.TestRPCRetryAndTimeout -v
```

### Teste individual

```bash
python -m unittest solinpy.client.test_client.TestSolanaRPCClient.test_get_health_success -v
```

### Saída esperada

```
test_no_retry_on_fatal_rpc_error ... ok
test_retry_exhausted_on_network_error ... ok
test_retry_on_http_429 ... ok
test_timeout_applied_to_config ... ok
test_endpoint_resolution ... ok
test_get_health_success ... ok
test_get_latest_blockhash ... ok
test_retry_on_network_error ... ok
test_rpc_error_response ... ok
test_send_transaction_payload ... ok

----------------------------------------------------------------------
Ran 10 tests in 1.XXXs

OK
```

## Estrutura de Arquivos

```
solinpy/client/
├── client.py        # SolanaRPCClient
├── entities.py      # RPCConfig
├── execptions.py    # RPCError
└── test_client.py   # Testes unitários
```

## Histórico de Alterações

### v0.1.0 — Refatoração de retry e tratamento de erros

- **Unificação do controle de retry** — loop usa agora apenas `max_retries` como limite (antes havia inconsistência entre `retries` e `max_retries`)
- **Tratamento explícito de `HTTPError`** — erros HTTP (como 429 Too Many) agora são capturados separadamente para permitir retry correto
- **Retry configurável por tipo de erro** — `retryable_http_codes` e `retryable_rpc_codes` permitem definir quais erros devem disparar retry
- **Backoff com jitter** — adicionado jitter aleatório (0–50%) para evitar thundering herd
- **Todas as exceções encapsuladas em `RPCError`** — elimina `ConnectionError` e `RuntimeError` como exceções públicas
- **Correção de testes** — testes agora usam `max_retries` e esperam `RPCError` corretamente
