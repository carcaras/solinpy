# 🤝 Contributing Guide — SolInPy

Python Framework for Solana focused on developer experience and simplicity.

---

## 📌 Features (MVP)

- RPC client
- Wallet management
- Transactions

---

## 📦 Development Setup

```bash
git clone https://github.com/your-org/solinpy.git
cd solinpy

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt
```

---

## 🧹 Code Quality Rules

This project enforces strict quality standards:

- Type checking: `mypy`
- Linting: `ruff`
- Testing: `pytest`

All contributions must pass CI before merge.

---

## 🚀 Running Checks Locally

### Lint

```bash
python -m ruff check .
```

### Format

```bash
python -m ruff format .
```

### Type Check

```bash
python -m mypy solinpy
```

### Tests

```bash
pytest
```

---

## 🔁 Recommended Workflow

```bash
git checkout -b feature/my-feature
```

Make changes, then:

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

Open a Pull Request.

---

## ⚠️ Pull Request Requirements

A PR will only be merged if:

- [ ] Ruff passes
- [ ] MyPy passes
- [ ] Tests pass
- [ ] Code is documented where necessary
- [ ] No untyped functions introduced
- [ ] No breaking changes without discussion

---

## 🧪 Testing Philosophy

- Unit tests for core logic
- Integration tests for RPC interactions
- Avoid mainnet dependency in tests
- Use devnet only for integration tests

---

## 📂 Project Structure

```
solinpy/
├── solinpy/
│   ├── client/
│   ├── wallet/
│   ├── transaction/
│   └── utils/
├── tests/
├── examples/
└── docs/
```

---

## 🧠 Engineering Philosophy

SolInPy is built on:

- Simplicity over complexity
- Developer experience first
- Predictable APIs
- Strong typing
- Reliability by design

---

## 🚀 Next Steps (Roadmap)

- RPC abstraction improvements
- Transaction builder expansion
- SPL token support
- Better error mapping
- CLI tooling (future)
