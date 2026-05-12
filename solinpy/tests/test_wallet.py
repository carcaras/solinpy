import json
from pathlib import Path
import pytest
from solders.keypair import Keypair
from solinpy.wallet.manager import WalletManager


def test_generate_keypair() -> None:
    """Test if a valid keypair is generated."""
    keypair = WalletManager.generate_keypair()
    assert isinstance(keypair, Keypair)
    # A chave secreta exportada no solders tem 64 bytes
    assert len(bytes(keypair)) == 64


def test_import_from_json(tmp_path: Path) -> None:
    """Test importing a keypair from a generated JSON file."""
    # Gera uma chave real para testar a importação
    original_keypair = Keypair()
    # O solders exporta a secret key que já contém os 64 bytes necessários
    secret_bytes = list(bytes(original_keypair))

    mock_file = tmp_path / "mock_wallet.json"
    with open(mock_file, "w", encoding="utf-8") as f:
        json.dump(secret_bytes, f)

    # Importa e verifica se a chave pública bate com a original
    imported_keypair = WalletManager.import_from_json(mock_file)
    assert imported_keypair.pubkey() == original_keypair.pubkey()


def test_import_from_json_file_not_found() -> None:
    """Test if the proper error is raised when file is missing."""
    with pytest.raises(FileNotFoundError):
        WalletManager.import_from_json("non_existent_path.json")


def test_import_from_json_invalid_format(tmp_path: Path) -> None:
    """Test if ValueError is raised for non-list JSON."""
    mock_file = tmp_path / "invalid_wallet.json"
    with open(mock_file, "w", encoding="utf-8") as f:
        json.dump({"invalid": True}, f)

    with pytest.raises(ValueError):
        WalletManager.import_from_json(mock_file)
