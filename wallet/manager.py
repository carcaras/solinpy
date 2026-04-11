import json
from pathlib import Path
from typing import Union
from solders.keypair import Keypair


class WalletManager:
    """Utility class to handle Solana wallet operations."""

    @staticmethod
    def generate_keypair() -> Keypair:
        """
        Creates a new Solana keypair.

        Returns:
            Keypair: A standard Solana keypair from the solders library.
        """
        return Keypair()

    @staticmethod
    def import_from_json(file_path: Union[str, Path]) -> Keypair:
        """
        Loads a keypair from a standard Solana CLI JSON file.

        Args:
            file_path: Path to the .json file.

        Returns:
            Keypair: The imported keypair object.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON data is not a valid list of bytes.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Invalid JSON format: expected a list of bytes")

        # solders utiliza from_bytes para reconstruir a chave
        return Keypair.from_bytes(bytes(data))
