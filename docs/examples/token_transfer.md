# Example: SPL Token Transfer

This practical example demonstrates how to transfer an SPL Token on the Solana Devnet using **SolInPy**. 

The framework automatically handles the derivation and creation of the receiver's Associated Token Account (ATA) if it does not exist.

```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solinpy.transaction.token import send_token_transfer

# 1. Initialize the client
client = Client("[https://api.devnet.solana.com](https://api.devnet.solana.com)")

# 2. Load your wallet (replace with actual bytes or file loading)
sender_keypair = Keypair() 

# 3. Define parameters
destination = "RECEIVER_WALLET_ADDRESS"
mint_address = "TOKEN_MINT_ADDRESS"

# 4. Execute transfer
signature = send_token_transfer(
    client=client,
    sender_keypair=sender_keypair,
    destination_wallet=destination,
    token_mint=mint_address,
    amount=1,
    decimals=9
)

print(f"Success! Signature: {signature.value}")