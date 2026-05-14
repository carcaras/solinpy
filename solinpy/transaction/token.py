from typing import Any
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import create_account
from spl.token.instructions import (
    InitializeMintParams,
    initialize_mint,
    transfer_checked,
    TransferCheckedParams,
    create_associated_token_account,
)
from spl.token.constants import MINT_LEN

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
        ASSOCIATED_TOKEN_PROGRAM_ID,
    )
    return ata


def send_token_transfer(
    client: Any,
    sender_keypair: Keypair,
    destination_wallet: str,
    token_mint: str,
    amount: int,
    decimals: int,
) -> Any:
    """
    Executes a complete SPL token transfer using the modern Solders architecture.
    """
    sender_pubkey = sender_keypair.pubkey()
    receiver_pubkey = Pubkey.from_string(destination_wallet)
    mint_pubkey = Pubkey.from_string(token_mint)

    # Derive ATAs
    sender_ata = get_associated_token_address(str(sender_pubkey), token_mint)
    receiver_ata = get_associated_token_address(destination_wallet, token_mint)

    instructions = []

    # Verify if receiver account exists
    account_info = client.get_account_info(receiver_ata)

    if account_info.value is None:
        # Adds instruction to create the account if it's missing
        create_ata_ix = create_associated_token_account(
            payer=sender_pubkey, owner=receiver_pubkey, mint=mint_pubkey
        )
        instructions.append(create_ata_ix)

    # Prepare transfer instruction
    transfer_ix = transfer_checked(
        TransferCheckedParams(
            program_id=TOKEN_PROGRAM_ID,
            source=sender_ata,
            mint=mint_pubkey,
            dest=receiver_ata,
            owner=sender_pubkey,
            amount=amount,
            decimals=decimals,
        )
    )
    instructions.append(transfer_ix)

    # Modern Solana Transaction Building
    # 1. Get the latest blockhash from the network
    recent_blockhash = client.get_latest_blockhash().value.blockhash

    # 2. Build the message with our instructions
    msg = Message(instructions, sender_pubkey)

    # 3. Create and sign the transaction
    tx = Transaction([sender_keypair], msg, recent_blockhash)

    # Finalize and send
    return client.send_transaction(tx)


def create_token_mint(
    client: Any,
    payer_keypair: Keypair,
    mint_authority_pubkey: Pubkey,
    decimals: int,
) -> tuple[Any, Pubkey]:
    """
    Creates and initializes a new SPL Token mint account.

    Args:
        client: Solana RPC client with methods used for rent, blockhash and tx send.
        payer_keypair: Fee payer and funding account.
        mint_authority_pubkey: Authority that can mint new tokens.
        decimals: Number of decimal places for the token mint.

    Returns:
        tuple[Any, Pubkey]: Transaction signature and the new mint address.
    """
    mint_keypair = Keypair()
    payer_pubkey = payer_keypair.pubkey()
    mint_pubkey = mint_keypair.pubkey()

    rent_response = client.get_minimum_balance_for_rent_exemption(MINT_LEN)
    rent_lamports = rent_response.value if hasattr(rent_response, "value") else rent_response

    create_mint_account_ix = create_account(
        {
            "from_pubkey": payer_pubkey,
            "to_pubkey": mint_pubkey,
            "lamports": rent_lamports,
            "space": MINT_LEN,
            "owner": TOKEN_PROGRAM_ID,
        }
    )

    initialize_mint_ix = initialize_mint(
        InitializeMintParams(
            decimals=decimals,
            program_id=TOKEN_PROGRAM_ID,
            mint=mint_pubkey,
            mint_authority=mint_authority_pubkey,
            freeze_authority=None,
        )
    )

    recent_blockhash = client.get_latest_blockhash().value.blockhash
    msg = Message([create_mint_account_ix, initialize_mint_ix], payer_pubkey)
    tx = Transaction([payer_keypair, mint_keypair], msg, recent_blockhash)

    signature = client.send_transaction(tx)
    return signature, mint_pubkey
