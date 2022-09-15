"""Verification class"""

from typing import Callable
from classes.block import Block
from classes.transactions import Transaction
from utils.hash_util import (
    hash_block,
    hash_string_256,
)


class Verification:
    """Verification class"""

    def valid_proof(
        self, transactions: list[Transaction], last_hash: str, proof: int
    ) -> bool:
        """returns whether a proof-of-work is valid

        Args:
            transaction (list): a list of transaction objects
            last_hash (string): the has string of the last block successfully mined
            proof (string): a string of numbers
        """
        guess = (
            str([txn.to_ordered_dict() for txn in transactions])
            + str(last_hash)
            + str(proof)
        ).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == "00"

    def verify_chain(self, blockchain: list[Block]) -> bool:
        """verifies the validity of the blockchain"""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                print("Block hash is not valid")
                return False
            if not self.valid_proof(
                block.transactions[:-1], block.previous_hash, block.proof
            ):
                print("Proof of work is not valid")
                return False
        return True

    def verify_transaction(
        self, transaction: Transaction, get_balances: Callable[[str], int]
    ) -> bool:
        """verifies transaction against sender's balance

        Args:
            transaction: the transaction to be verified
        """
        sender_balance = get_balances(transaction.sender)
        return sender_balance >= transaction.amount

    def verify_transactions(
        self, open_transactions: list[Transaction], get_balances: Callable[[str], int]
    ) -> str:
        """verifies all open transactions"""
        return all(
            self.verify_transaction(tx, get_balances) for tx in open_transactions
        )
