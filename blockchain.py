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


def get_user_input():
    """gets user input about transaction amount
    """
    tx_amount = float(input("Type the value of the transaction: "))
    if len(blockchain) <= 0:
        add_value(tx_amount, [1.0])
    else:
        add_value(tx_amount, get_last_blockchain_value())


for item in range(3):
    get_user_input()


print(blockchain)
