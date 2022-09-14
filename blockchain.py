"""blockchain script"""

import json
from functools import reduce
from collections import OrderedDict
from utils.hash_util import hash_string_256, hash_block
from classes.block import Block

MINING_REWARD = 10
blockchain = []
open_transactions = []
OWNER = "Uriel"
participants = {OWNER}


def load_data():
    """loads blockchain data from file"""
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r", encoding="utf-8") as blockchain_file:
            # file_content = pickle.loads(blockchain_file.read())
            file_content = blockchain_file.readlines()

            # blockchain = file_content["chain"]
            # open_transactions = file_content["ot"]
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_txs = [
                    OrderedDict(
                        [
                            ("sender", tx["sender"]),
                            ("recipient", tx["recipient"]),
                            ("amount", tx["amount"]),
                        ]
                    )
                    for tx in block["transactions"]
                ]
                updated_block = Block(
                    block["index"],
                    block["previous_hash"],
                    converted_txs,
                    block["proof"],
                    block["timestamp"],
                )
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for txn in open_transactions:
                updated_transaction = OrderedDict(
                    [
                        ("sender", txn["sender"]),
                        ("recipient", txn["recipient"]),
                        ("amount", txn["amount"]),
                    ]
                )
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        genesis_block = Block(0, "", [], 100)
        blockchain = [genesis_block]
        open_transactions = []


load_data()


def save_data():
    """saves blockchain data to file"""
    try:
        with open("blockchain.txt", mode="w", encoding="utf-8") as blockchain_file:
            saveable_chain = [block.__dict__ for block in blockchain]
            blockchain_file.write(json.dumps(saveable_chain))
            blockchain_file.write("\n")
            blockchain_file.write(json.dumps(open_transactions))
            # data_to_save = {"chain": blockchain, "ot": open_transactions}
            # blockchain_file.write(pickle.dumps(data_to_save))
    except (IOError, IndexError):
        print("Saving failed!")


def get_last_blockchain_value():
    """gets last blockchain value

    Returns:
        float: the last blockchain value
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction) -> bool:
    """verifies transaction against sender's balance

    Args:
        transaction: the transaction to be verified
    """
    sender_balance = get_balances(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(sender: str, recipient: str, amount: float = 1.0) -> bool:
    """add transaction to blockchain

    Args:
        sender (str): the sender name,
        recipient (str): the recipient name,
        amount (float): the amount to add to the blockchain
    """
    transaction = OrderedDict(
        [("sender", sender), ("recipient", recipient), ("amount", amount)]
    )
    if verify_transaction(transaction):
        participants.add(sender)
        participants.add(recipient)
        open_transactions.append(transaction)
        return True
    return False


def get_balances(participant: str) -> int:
    """gets a participants' balance form the blockchain

    Args:
        participant (string): the participant's name

    Returns:
        int: participants' balance
    """
    tx_sender = [
        [tx["amount"] for tx in block.transactions if tx["sender"] == participant]
        for block in blockchain
    ]
    open_tx_sender = [
        tx["amount"] for tx in open_transactions if tx["sender"] == participant
    ]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
        if len(tx_amount) > 0
        else tx_sum + 0,
        tx_sender,
        0,
    )

    tx_recipient = [
        [tx["amount"] for tx in block.transactions if tx["recipient"] == participant]
        for block in blockchain
    ]
    amount_received = reduce(
        lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
        if len(tx_amount) > 0
        else tx_sum + 0,
        tx_recipient,
        0,
    )

    return amount_received - amount_sent


def valid_proof(transactions, last_hash, proof) -> bool:
    """returns whether a proof-of-work is valid

    Args:
        transaction (list): a list of transaction objects
        last_hash (string): the has string of the last block successfully mined
        proof (string): a string of numbers
    """
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == "00"


def proof_of_work() -> int:
    """executes proof-of-work algorithm

    Returns:
        int: the number that satisfies the proof-of-work algorithm
    """
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block() -> bool:
    """mines a block in the blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict(
        [("sender", "MINING"), ("recipient", OWNER), ("amount", MINING_REWARD)]
    )
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def handle_transaction():
    """gets user input for a new transaction"""
    amount_text = input("Type the amount of the transaction: ")
    # sender_name = input("Type the name of the sender: ")
    recipient_name = input("Type the name of the recipient: ")

    try:
        tx_amount = float(amount_text)
        print(
            "\n\nAdding a "
            + str(tx_amount)
            + " transaction from "
            + OWNER
            + " to "
            + recipient_name
            + " to the blockchain...\n\n"
        )
    except ValueError:
        print("ERROR: That amount is not a number!")
        input()
        return

    if add_transaction(OWNER, recipient_name, tx_amount):
        print("\n\nDONE!")
        input("Click to continue...")
    else:
        print("Transaction failed for lack of funds!")


def get_user_choice():
    """Get the user choice program choice

    Returns:
        string: the choice the user entered
    """
    return input("Your choice: ")


def print_blockchain_blocks():
    """Prints all the blocks in the blockchain"""
    for index, block in enumerate(blockchain):
        print(20 * "-")
        print("Outputting block number: " + str(index + 1))
        print(block.__dict__)
        print(20 * "-")
    print("\n\nDONE!")
    input("Click to continue...")


def verify_chain() -> bool:
    """verifies the validity of the blockchain"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            print("Block hash is not valid")
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of work is not valid")
            return False
    return True


COMMAND = ""
while COMMAND != "exit":
    print("\nChoose the command you want to execute...")
    print("EXIT: exits the program")
    print("TRANS: includes a new pending transaction")
    print("MINE: mines a new block")
    print("PART: prints all the participants in the blockchain")
    print("PRINT: prints all the blocks in the blockchain\n")
    COMMAND = get_user_choice()

    if not verify_chain():
        print_blockchain_blocks()
        print("The chain is invalid!")
        break

    match COMMAND:
        case "exit" | "EXIT":
            continue
        case "trans" | "TRANS":
            handle_transaction()
        case "print" | "PRINT":
            print_blockchain_blocks()
        case "mine" | "MINE":
            if mine_block():
                print("Block mined!")
                open_transactions = []
                print("Open transactions cleaned up")
                save_data()
                print("Data saved!")
        case "part" | "PART":
            print(participants)
        case _:
            print("That's not a command. Try again")

    print(f"\nBalances for {OWNER}: {get_balances(OWNER):6.2f}")
