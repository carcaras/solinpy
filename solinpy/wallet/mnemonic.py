
import hmac
import hashlib
import struct
import gc
from mnemonic import Mnemonic
from solders.keypair import Keypair



def import_from_mnemonic(
    mnemonic_str: str,
    passphrase: str = "",
    derivation_path: str = "m/44'/501'/0'/0'"
) -> Keypair:
    """Reconstrói uma Keypair Solana a partir de uma seed phrase BIP39."""
    if not isinstance(mnemonic_str, str):
        raise ValueError("Mnemonic must be a string")

    words = mnemonic_str.strip().split()
    if len(words) not in (12, 18, 24):
        raise ValueError("Invalid mnemonic length: must be 12, 18 or 24 words")
    
    if not Mnemonic("english").check(mnemonic_str.strip()):
        raise ValueError("Invalid mnemonic: checksum or wordlist mismatch")
    
    seed = Mnemonic("english").to_seed(mnemonic_str.strip(), passphrase=passphrase)
    private_key = _derive_slip10_ed25519(seed, derivation_path)

    keypair = Keypair.from_seed(private_key)

    del seed, private_key
    gc.collect()
    return keypair

def _derive_slip10_ed25519(seed: bytes, path: str) -> bytes:
    """Internal derivation SLIP-0010 to  Ed25519 (hardened only)."""
    master = hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
    key, chain = master[:32], master[32:]

    parts = path.strip().split("/")
    if parts[0] != "m":
        raise ValueError("Derivation path must start with 'm'")

    for part in parts[1:]:
        if not part.endswith("'"):
            raise ValueError("Ed25519 derivation requires hardened indices (e.g., 0')")

        index = int(part[:-1]) | 0x80000000
        data = b"\x00" + key + struct.pack(">I", index)
        mac = hmac.new(chain, data, hashlib.sha512).digest()
        key, chain = mac[:32], mac[32:]
    return key