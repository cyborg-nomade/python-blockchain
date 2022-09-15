"""Defines a blockchain block"""

from time import time
from classes.printable import Printable
from classes.transactions import Transaction


class Block(Printable):
    """Defines a blockchain block"""

    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: list[Transaction],
        proof: int,
        timestamp=None,
    ) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp
