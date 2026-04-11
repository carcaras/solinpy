from solpy.utils.convert import sol_to_lamports
from solpy.transaction.transaction import TransactionBuilder


def transfer_sol(client, from_wallet, to_address: str, amount_sol: float):
    lamports = sol_to_lamports(amount_sol)

    instruction = {
        "type": "transfer",
        "from": from_wallet.public_key,
        "to": to_address,
        "lamports": lamports,
    }

    tx = TransactionBuilder().add_instruction(instruction).build(from_wallet)

    signed_tx = tx.signer.sign(tx)

    return client.send_transaction(signed_tx)
