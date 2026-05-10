# SolInPy

SolInPy é um SDK Python para Solana pensado para simplificar o dia a dia de quem precisa falar com a rede sem montar tudo do zero.

Ele resolve três pontos principais:

- acesso ao JSON-RPC da Solana com retries, timeouts e tratamento de erro;
- criação e importação de carteiras;
- helpers para airdrop e transferência de SPL tokens.

O objetivo é ser um ponto de entrada simples para protótipos, automações e integrações pequenas em devnet, testnet ou mainnet.

## O que o SDK cobre

- Cliente RPC: `SolanaRPCClient`
- Configuração de rede: `RPCConfig`
- Carteiras: `WalletManager`
- Airdrop em redes de teste: `create_airdrop` e `request_airdrop`
- Transferência de SPL tokens: `send_token_transfer`
- Decodificação de contas: utilitários em `solinpy.utils.account_decoder`

## Requisitos

- Python 3.10+
- acesso à internet para chamadas RPC reais

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone <url-do-repositorio>
cd solana-hackathon

python -m venv .venv
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -r requirements.txt
```

Se estiver no Windows, ative o ambiente com:

```bash
.venv\Scripts\activate
```

Depois disso, execute seus scripts a partir da raiz do projeto para que o pacote `solinpy` seja importado corretamente.

## Quickstart

### 1. Fazer uma chamada RPC básica

```python
from solinpy.client.client import SolanaRPCClient
from solinpy.client.entities import RPCConfig

client = SolanaRPCClient(RPCConfig(cluster="devnet"))

print(client.get_health())
print(client.get_latest_blockhash())
```

### 2. Criar ou importar uma carteira

```python
from solinpy.wallet.manager import WalletManager

keypair = WalletManager.generate_keypair()
print(keypair.pubkey())

loaded_keypair = WalletManager.import_from_json("my-wallet.json")
print(loaded_keypair.pubkey())
```

### 3. Pedir airdrop em devnet

```python
from solinpy.utils.airdrop import request_airdrop

result = request_airdrop(keypair, cluster="devnet")
print(result["signature"])
print(result["balance"])
```

### 4. Ler saldo e histórico

```python
wallet_address = str(keypair.pubkey())

print(client.get_balance(wallet_address))
print(client.get_sol_balance(wallet_address))
print(client.get_transaction_history(wallet_address, limit=5))
```

### 5. Transferir SPL token

```python
from solinpy.transaction.token import send_token_transfer

signature = send_token_transfer(
	client=client,
	sender_keypair=keypair,
	destination_wallet="<endereco-da-carteira-destino>",
	token_mint="<mint-do-token>",
	amount=25,
	decimals=6,
)

print(signature)
```

Esse helper cria a associated token account do destinatário automaticamente quando ela ainda não existir.

## Exemplo completo

```python
from solinpy.client.client import SolanaRPCClient
from solinpy.client.entities import RPCConfig
from solinpy.utils.airdrop import request_airdrop
from solinpy.wallet.manager import WalletManager

config = RPCConfig(cluster="devnet")
client = SolanaRPCClient(config)

wallet = WalletManager.generate_keypair()
airdrop = request_airdrop(wallet, cluster="devnet")

address = str(wallet.pubkey())
balance_lamports = client.get_balance(address)

print("Airdrop:", airdrop["signature"])
print("Saldo em lamports:", balance_lamports)
print("Saldo em SOL:", client.get_sol_balance(address))
```

## Estrutura do projeto

```text
solinpy/
├── client/
├── wallet/
├── transaction/
└── utils/
```

## Notas de uso

- `devnet` e `testnet` são as redes mais seguras para começar.
- `request_airdrop` e `create_airdrop` só fazem sentido nessas redes.
- `send_token_transfer` pressupõe que você já tem o mint do token e a carteira do destinatário.

## Contribuição

Os testes do projeto usam `pytest`, e a base também é verificada com `ruff` e `mypy`.

```bash
pytest
python -m ruff check .
python -m mypy solinpy
```
