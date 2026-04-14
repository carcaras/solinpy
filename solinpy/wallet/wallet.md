
# 🔐 Implementação: Importação de Carteira via Mnemônico (BIP39)

## 📖 Visão Geral
Este módulo permite a reconstrução de carteiras Solana a partir de **seed phrases BIP39** (12, 18 ou 24 palavras), seguindo o padrão de derivação **SLIP-0010 para Ed25519**. A implementação é compatível com wallets populares (Phantom, Solflare, Backpack) e com a CLI oficial da Solana.

---

## 🏗️ Arquitetura & Decisões de Design

| Decisão | Justificativa |
|---------|---------------|
| **Separação em `mnemonic.py`** | Isola lógica criptográfica pesada de `manager.py`, mantendo a fachada limpa e facilitando auditoria. |
| **SLIP-0010 em vez de BIP32** | A Solana usa exclusivamente a curva **Ed25519**, que não é compatível com BIP32. SLIP-0010 é o padrão correto para derivação nesta curva. |
| **Índices Hardened Obrigatórios** | Ed25519 não suporta derivação pública não-hardened. O módulo rejeita caminhos sem `'` para evitar chaves inválidas. |
| **Output direto para `solders.Keypair`** | Garante compatibilidade nativa com serialização, assinatura e envio de transações no ecossistema Rust/Python. |
| **Zero acoplamento com RPC** | O módulo não conhece endpoints, clusters ou HTTP. Segue o princípio *Single Responsibility*. |

---

## 📐 Especificações Técnicas

| Componente | Padrão | Detalhes |
|------------|--------|----------|
| **Wordlist** | BIP39 (English) | 2048 palavras, checksum integrado |
| **KDF** | PBKDF2-HMAC-SHA512 | 2048 iterações, salt = `"mnemonic" + passphrase` |
| **Derivação** | SLIP-0010 (Ed25519) | Master key via `HMAC-SHA512(key="ed25519 seed", msg=seed)` |
| **Path Padrão** | `m/44'/501'/0'/0'` | Coin type `501` (Solana), hardened em
Aqui está um documento técnico pronto para ser salvo como `docs/wallet/MNEMONIC_IMPLEMENTATION.md` ou na raiz do módulo. Ele cobre arquitetura, especificações criptográficas, segurança e integração.

---

# 🔐 Implementação: Importação de Carteira via Mnemônico (BIP39)

## 📖 Visão Geral
Este módulo permite a reconstrução de carteiras Solana a partir de **seed phrases BIP39** (12, 18 ou 24 palavras), seguindo o padrão de derivação **SLIP-0010 para Ed25519**. A implementação é compatível com wallets populares (Phantom, Solflare, Backpack) e com a CLI oficial da Solana.

---

## 🏗️ Arquitetura & Decisões de Design

| Decisão | Justificativa |
|---------|---------------|
| **Separação em `mnemonic.py`** | Isola lógica criptográfica pesada de `manager.py`, mantendo a fachada limpa e facilitando auditoria. |
| **SLIP-0010 em vez de BIP32** | A Solana usa exclusivamente a curva **Ed25519**, que não é compatível com BIP32. SLIP-0010 é o padrão correto para derivação nesta curva. |
| **Índices Hardened Obrigatórios** | Ed25519 não suporta derivação pública não-hardened. O módulo rejeita caminhos sem `'` para evitar chaves inválidas. |
| **Output direto para `solders.Keypair`** | Garante compatibilidade nativa com serialização, assinatura e envio de transações no ecossistema Rust/Python. |
| **Zero acoplamento com RPC** | O módulo não conhece endpoints, clusters ou HTTP. Segue o princípio *Single Responsibility*. |

---

## 📐 Especificações Técnicas

| Componente | Padrão | Detalhes |
|------------|--------|----------|
| **Wordlist** | BIP39 (English) | 2048 palavras, checksum integrado |
| **KDF** | PBKDF2-HMAC-SHA512 | 2048 iterações, salt = `"mnemonic" + passphrase` |
| **Derivação** | SLIP-0010 (Ed25519) | Master key via `HMAC-SHA512(key="ed25519 seed", msg=seed)` |
| **Path Padrão** | `m/44'/501'/0'/0'` | Coin type `501` (Solana), hardened em todos os níveis |
| **Formato de Saída** | `solders.keypair.Keypair` | 64 bytes (32 secret + 32 public) |

---

## 📦 Dependências

```toml
[project.dependencies]
solders = ">=0.22,<0.23"
mnemonic = ">=1.1.0"
```
> 💡 `mnemonic` é a referência leve (~50KB) e mantida para BIP39 em Python. Evita reimplementação insegura de checksum e PBKDF2.

---

## 💻 Exemplos de Uso

### Importação Básica
```python
from solinpy.wallet.mnemonic import import_from_mnemonic

mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
keypair = import_from_mnemonic(mnemonic)

print("🔑 Public Key:", keypair.pubkey())
```

### Com Passphrase (25ª palavra)
```python
keypair = import_from_mnemonic(
    mnemonic_str="word1 word2 ... word12",
    passphrase="minha_senha_secreta"
)
```

### Path Customizado (Avançado)
```python
keypair = import_from_mnemonic(
    mnemonic_str="word1 word2 ... word12",
    derivation_path="m/44'/501'/1'/0'"  # Conta 2, endereço 0
)
```

---

## 🔒 Considerações de Segurança

| Prática | Implementação |
|---------|---------------|
| **Validação Estrita** | Verifica tamanho (12/18/24), checksum BIP39 e wordlist antes de derivar |
| **Hardened Only** | Rejeita caminhos como `m/44/501/0/0` (Ed25519 não os suporta) |
| **Limpeza de Memória** | `del seed, private_key` + `gc.collect()` após criação da `Keypair` |
| **Zero Log de Chaves** | Nenhum dado sensível é impresso, serializado ou salvo em cache |
| **Sem Fallback Inseguro** | Erros de checksum/path levantam `ValueError` imediato, sem tentativas de correção automática |

> ⚠️ **Atenção:** Em ambientes de produção com alta criticidade, considere usar `mlock()` ou enclaves (SGX/TrustZone) para zeroar memória de forma garantida pelo SO.

---

## 🧪 Validação & Testes

### Vetor Oficial de Compatibilidade
```python
from solinpy.wallet.mnemonic import import_from_mnemonic

kp = import_from_mnemonic("abandon " * 11 + "about")
assert str(kp.pubkey()) == "3h1zGmCwsRJnVk5BuRNMLsPaQu1y2aqXqXDWYCgrp5UG"
```

### Casos de Falha Cobertos
| Entrada | Comportamento Esperado |
|---------|------------------------|
| 11 palavras | `ValueError: Invalid mnemonic length` |
| Checksum inválido | `ValueError: Invalid mnemonic: checksum or wordlist mismatch` |
| Path sem `'` | `ValueError: Ed25519 derivation requires hardened indices` |
| `passphrase=None` | `ValueError: Mnemonic must be a string` |

---

## 🔗 Integração com o Framework

```text
[mnemonic.py] → import_from_mnemonic() → Keypair (solders)
       ↓
[manager.py] → Wrapper opcional ou uso direto
       ↓
[client.py]  → Recebe tx assinada (base64) → sendTransaction()
```
- **Contrato:** O módulo de mnemônicos retorna `Keypair`. A assinatura e serialização ficam a cargo do módulo de transações.
- **Desacoplamento:** Trocar `mnemonic.py` por um módulo de hardware wallet (Ledger/Trezor) não exige alterações em `client.py`.

---

## 🐛 Solução de Problemas

| Sintoma | Causa Provável | Solução |
|---------|----------------|---------|
| `Checksum mismatch` | Palavra errada ou ordem trocada | Verificar wordlist BIP39 oficial. Usar `mnemonic.Mnemonic.check()` para debug |
| `Index must be hardened` | Path sem `'` no final de cada nível | Usar formato `m/44'/501'/X'/Y'` |
| `solders.KeyError` | Seed de 32 bytes inválida | Confirmar que a derivação SLIP-0010 foi executada corretamente |
| `ImportError: mnemonic` | Dependência não instalada | `pip install mnemonic` ou atualizar `pyproject.toml` |

