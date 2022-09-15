"""utility functions for hashing blockchain blocks
"""

import hashlib
import json

from classes.block import Block


def hash_string_256(string: str) -> str:
    """returns the SHA256 hash string of the given string

    Args:
        string (string): the string to be hashed

    Returns:
        string: the string hashed
    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block: Block) -> str:
    """Returns the hashed string of the block

    Args:
        block: the block to be hashed

    Returns:
        string: the string hash of the block
    """
    hashabled_block = block.__dict__.copy()
    hashabled_block["transactions"] = [
        tx.to_ordered_dict() for tx in hashabled_block["transactions"]
    ]
    return hash_string_256(json.dumps(hashabled_block, sort_keys=True).encode())
