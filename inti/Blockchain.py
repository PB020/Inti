from . import Inti
import json
import time


class Blockchain:
    # Dificulty of PoW algorithm
    difficulty = 2

    def __init__(self) -> None:
        """
        Constructor for the Blockchain class
        """
        self.chain = []
        self.genesis()
        self.unconfirmed_transactions = []

    def genesis(self) -> None:
        """
        Generates the genesis block and appends it to the chain
        """
        genesis = Inti.Inti(0, [], time.time(), "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @property
    def previous_block(self) -> Inti.Inti:
        """
        Retrieves the most recent block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, block: Inti.Inti) -> str:
        """
        Tries different values of the nonce to get a hash that
        satisfies the difficulty criteria
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def proof_validation(self, block: Inti.Inti, block_hash: str) -> bool:
        """
        Check if block_hash is valid and satisfies the difficulty criteria
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_block(self, block: Inti.Inti, proof: str) -> bool:
        """
        Adds a block onto the chain after verification
        (proof and previous hash validation)
        """
        previous_hash = self.previous_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.proof_validation(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction: str) -> None:
        """
        Adds new transactions to the blockchain's unconfirmed list
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self) -> int:
        """
        Interface to add pending transactions to the blockchain
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        new_block = Inti.Inti(index=last_block.index + 1,
                              transactions=self.unconfirmed_transactions,
                              timestamp=time.time(),
                              previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def check_chain_validity(cls, chain) -> bool:
        """
        Checks if the entire blockchain is valid
        """
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            delattr(block, "hash")

            if not cls.proof_validation(block, block.hash) or previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result
