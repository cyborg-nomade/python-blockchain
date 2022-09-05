"""blockchain script"""

GENESIS_BLOCK = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}
blockchain = [GENESIS_BLOCK]
open_transactions = []
OWNER = "Uriel"
participants = {OWNER}


def get_last_blockchain_value():
    """gets last blockchain value

    Returns:
        float: the last blockchain value
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount=1.0):
    """add transaction to blockchain

    Args:
      sender (str): the sender name,
      recipient (str): the recipient name,
      amount (float): the amount to add to the blockchain
    """
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    participants.add(sender)
    participants.add(recipient)
    open_transactions.append(transaction)


def hash_block(block):
    """Returns the hash of the block

    Args:
        block: the block to be hashed

    Returns:
        string: the hash of the block
    """
    return "-".join([str(item[1]) for item in block.items()])


def mine_block():
    """mines a block in the blockchain"""
    last_block = blockchain[-1]
    hash_mock = hash_block(last_block)
    print(hash_mock)
    block = {
        "previous_hash": hash_mock,
        "index": len(blockchain),
        "transactions": open_transactions,
    }
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

    add_transaction(OWNER, recipient_name, tx_amount)
    print("DONE!")
    input("Click to continue...")


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
        case "part" | "PART":
            print(participants)
        case _:
            print("That's not a command. Try again")
