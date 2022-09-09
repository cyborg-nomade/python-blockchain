"""utility functions for hashing blockchain blocks
"""

import hashlib
import json


def hash_string_256(string):
    """returns the SHA256 hash string of the given string

    Args:
        string (string): the string to be hashed

    Returns:
        string: the string hashed
    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Returns the hashed string of the block

    Args:
        block: the block to be hashed

    Returns:
        string: the string hash of the block
    """
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
