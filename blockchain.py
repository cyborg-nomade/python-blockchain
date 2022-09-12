"""blockchain script"""

from functools import reduce
from collections import OrderedDict
from utils.hash_util import hash_string_256, hash_block
import json

MINING_REWARD = 10
GENESIS_BLOCK = {"previous_hash": "", "index": 0, "transactions": [], "proof": 100}
blockchain = [GENESIS_BLOCK]
open_transactions = []
OWNER = "Uriel"
participants = {OWNER}


def load_data():
    """loads blockchain data from file"""
    with open("blockchain.txt", mode="r", encoding="utf-8") as blockchain_file:
        file_content = blockchain_file.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                "previous_hash": block["previous_hash"],
                "index": block["index"],
                "proof": block["proof"],
                "transactions": [
                    OrderedDict(
                        [
                            ("sender", tx["sender"]),
                            ("recipient", tx["recipient"]),
                            ("amount", tx["amount"]),
                        ]
                    )
                    for tx in block["transactions"]
                ],
            }
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


load_data()


def save_data():
    """saves blockchain data to file"""
    with open("blockchain.txt", mode="w", encoding="utf-8") as blockchain_file:
        blockchain_file.write(json.dumps(blockchain))
        blockchain_file.write("\n")
        blockchain_file.write(json.dumps(open_transactions))


def get_last_blockchain_value():
    """gets last blockchain value

    Returns:
        float: the last blockchain value
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """verifies transaction against sender's balance

    Args:
        transaction: the transaction to be verified
    """
    sender_balance = get_balances(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(sender, recipient, amount=1.0):
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


def get_balances(participant):
    """gets a participants' balance form the blockchain

    Args:
        participant (string): the participant's name

    Returns:
        int: participants' balance
    """
    tx_sender = [
        [tx["amount"] for tx in block["transactions"] if tx["sender"] == participant]
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
        [tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant]
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


def valid_proof(transactions, last_hash, proof):
    """returns whether a proof-of-work is valid

    Args:
        transaction (list): a list of transaction objects
        last_hash (string): the has string of the last block successfully mined
        proof (string): a string of numbers
    """
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == "00"


def proof_of_work():
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


def mine_block():
    """mines a block in the blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict(
        [("sender", "MINING"), ("recipient", OWNER), ("amount", MINING_REWARD)]
    )
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions,
        "proof": proof,
    }
    blockchain.append(block)
    save_data()
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
        print("DONE!")
        input("Click to continue...")
    else:
        print("Transaction failed for lack of funds!")
    print(open_transactions)


def get_user_choice():
    """Get the user choice program choice

    Returns:
        string: the choice the user entered
    """
    return input("Your choice: ")


def print_blockchain_blocks():
    """Prints all the blocks in the blockchain"""
    for index, block in enumerate(blockchain):
        print("Outputting block number: " + str(index + 1))
        print(block)
    print("\n\nDONE!")
    input("Click to continue...")


def verify_chain():
    """verifies the validity of the blockchain"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(
            block["transactions"][:-1], block["previous_hash"], block["proof"]
        ):
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

    print("You chose: " + COMMAND + "\n")

    if not verify_chain():
        print_blockchain_blocks()
        print("The chain is invalid!")
        break

    print(f"Balances for {OWNER}: {get_balances(OWNER):6.2f}")

    match COMMAND:
        case "exit" | "EXIT":
            continue
        case "trans" | "TRANS":
            handle_transaction()
        case "print" | "PRINT":
            print_blockchain_blocks()
        case "mine" | "MINE":
            if mine_block():
                open_transactions = []
                save_data()
        case "part" | "PART":
            print(participants)
        case _:
            print("That's not a command. Try again")
