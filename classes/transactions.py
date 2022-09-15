"""Defines a transactions in the blockchain"""


from collections import OrderedDict

from classes.printable import Printable


class Transaction(Printable):
    """Defines a transactions in the blockchain"""

    def __init__(self, sender: str, recipient: str, amount: float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        """Converts transaction to OrderedDict"""
        return OrderedDict(
            [
                ("sender", self.sender),
                ("recipient", self.recipient),
                ("amount", self.amount),
            ]
        )
