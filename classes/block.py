"""Defines a blockchain block"""

from time import time
from typing import Any


class Block:
    """Defines a blockchain block"""

    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: list[Any],
        proof: int,
        time=time(),
    ) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time
