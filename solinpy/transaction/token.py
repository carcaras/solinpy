import base64
from typing import Any
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.hash import Hash
from spl.token.instructions import (
    transfer_checked, 
    TransferCheckedParams, 
    create_associated_token_account
)

# Constants for SPL Token Program
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOCIATED_TOKEN_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")

def get_associated_token_address(owner_address: str, token_mint_address: str) -> Pubkey:
    """
    Derives the ATA (Associated Token Account) for the given wallet and mint.
    """
    owner_pubkey = Pubkey.from_string(owner_address)
    mint_pubkey = Pubkey.from_string(token_mint_address)
    
    ata, _ = Pubkey.find_program_address(
        [bytes(owner_pubkey), bytes(TOKEN_PROGRAM_ID), bytes(mint_pubkey)],
        ASSOCIATED_TOKEN_PROGRAM_ID
    )
    return ata

def send_token_transfer(
    client: Any, 
    sender_keypair: Keypair, 
    destination_wallet: str, 
    token_mint: str, 
    amount: int, 
    decimals: int
) -> Any:
    """
    Executes a complete SPL token transfer using the modern Versioned Transaction (V0) architecture.
    """
    sender_pubkey = sender_keypair.pubkey()
    receiver_pubkey = Pubkey.from_string(destination_wallet)
    mint_pubkey = Pubkey.from_string(token_mint)

    # 1. Derive ATAs for sender and receiver
    sender_ata = get_associated_token_address(str(sender_pubkey), token_mint)
    receiver_ata = get_associated_token_address(destination_wallet, token_mint)

    instructions = []

    # 2. Check if receiver's ATA exists
    account_info = client.get_account_info(receiver_ata)
    
    if account_info.get("result", {}).get("value") is None:
        # Adds instruction to create the ATA if missing
        create_ata_ix = create_associated_token_account(
            payer=sender_pubkey,
            owner=receiver_pubkey,
            mint=mint_pubkey
        )
        instructions.append(create_ata_ix)

    # 3. Prepare the transfer instruction
    transfer_ix = transfer_checked(
        TransferCheckedParams(
            program_id=TOKEN_PROGRAM_ID,
            source=sender_ata,
            mint=mint_pubkey,
            dest=receiver_ata,
            owner=sender_pubkey,
            amount=int(amount), # Ensure amount is an integer
            decimals=decimals
        )
    )
    instructions.append(transfer_ix)

    # 4. Modern Transaction Building (V0)
    # Fetch the latest blockhash and convert to Hash object
    raw_hash = client.get_latest_blockhash()
    recent_blockhash = Hash.from_string(raw_hash)
    
    # Compile the message correctly including the blockhash
    msg = MessageV0.try_compile(
        payer=sender_pubkey,
        instructions=instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash
    )
    
    # Sign the versioned transaction
    tx = VersionedTransaction(msg, [sender_keypair])

    # 5. Finalize: Encode to base64 and send via RPC
    return client.send_transaction(base64.b64encode(bytes(tx)).decode('utf-8'))