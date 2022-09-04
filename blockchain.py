"""blockchain script"""

blockchain = []


def get_last_blockchain_value():
    """gets last blockchain value

    Returns:
        float: the last blockchain value
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction_value):
    """add transaction to blockchain

    Args:
      transaction_amount (int): the amount to add to the blockchain
      last_transaction_value (list): last blockchain value
    """

    if last_transaction_value is None:
        last_transaction_value = [1.0]
    blockchain.append([last_transaction_value, transaction_amount])


def handle_transaction():
    """gets user input"""
    input_text = input("Type the value of the transaction: ")

    try:
        tx_amount = float(input_text)
        print(
            "\n\nAdding a " + str(tx_amount) + " transaction to the blockchain...\n\n"
        )
    except ValueError:
        print("ERROR: That is not a number!")
        input()
        return

    add_transaction(tx_amount, get_last_blockchain_value())
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


COMMAND = ""
while COMMAND != "exit":
    print("\nChoose the command you want to execute...")
    print("EXIT: exits the program")
    print("TRANS: includes a new transaction in the blockchain")
    print("PRINT: prints all the blocks in the blockchain\n")
    COMMAND = get_user_choice()

    print("You chose: " + COMMAND + "\n")

    match COMMAND:
        case "exit" | "EXIT":
            continue
        case "trans" | "TRANS":
            handle_transaction()
        case "print" | "PRINT":
            print_blockchain_blocks()
        case _:
            print("That's not a command. Try again")
