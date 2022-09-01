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


def get_user_input():
    """gets user input about transaction amount"""
    tx_amount = float(input("Type the value of the transaction: "))
    add_transaction(tx_amount, get_last_blockchain_value())


for item in range(3):
    get_user_input()


print(blockchain)
