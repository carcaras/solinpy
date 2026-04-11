from dataclasses import dataclass
from typing import List, Any


@dataclass
class Transaction:
    instructions: List[Any]
    signer: Any


class TransactionBuilder:
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)
        return self

    def build(self, signer):
        return Transaction(instructions=self.instructions, signer=signer)


def sign_transaction(transaction: Transaction):
    # aqui depois entra solders / solana-py
    signed = {"tx": transaction, "signed": True}
    return signed
