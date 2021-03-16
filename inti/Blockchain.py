import Inti
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
