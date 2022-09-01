"""blockchain script"""

blockchain = []


def get_last_blockchain_value():
    """gets last blockchain value

    Args:
        blockchain (list[float]): the blockchain list[float]

    Returns:
        float: the last blockchain value
    """
    return blockchain[-1]


def add_value(transaction_amount, last_transaction_value):
    """add value to blockchain"""
    blockchain.append([last_transaction_value, transaction_amount])


def add_transaction():
    """gets user input
    """
    input_text = input("Type the value of the transaction: ")

    try:
        tx_amount = float(input_text)
        print("\n\nAdding a " + str(tx_amount) +
              " transaction to the blockchain...\n\n")
    except ValueError:
        print("ERROR: That is not a number!")
        input()
        return

    if len(blockchain) <= 0:
        add_value(tx_amount, [1.0])
    else:
        add_value(tx_amount, get_last_blockchain_value())
    print("DONE!")
    input()


def get_user_choice():
    """Get the user choice program choice

    Returns:
        string: the choice the user entered
    """
    return input("Your choice: ")


def print_blockchain_blocks():
    """Prints all the blocks in the blockchain
    """
    for block in blockchain:
        print("Outputting block...")
        print(block)
    print("DONE!")
    input()


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
            add_transaction()
        case "print" | "PRINT":
            print_blockchain_blocks()
        case _:
            print("That's not a command. Try again")
