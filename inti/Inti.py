from hashlib import sha256
import json


class Inti:
    def __init__(self, index: int, transactions: list, timestamp: float, previous_hash: str) -> None:
        """
        Constructor for the block class 'Inti'
        :param index: Unique block ID
        :param transactions: List of transactions
        :param timestamp: Time of block generation
        :param previous_hash: Hash of the previous block in the chain
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self) -> str:
        """
        Returns JSON string of the block's hash
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
