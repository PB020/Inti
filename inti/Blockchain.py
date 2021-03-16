from inti.Inti import Inti
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
        genesis = Inti(0, [], time.time(), "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @property
    def previous_block(self) -> Inti:
        """
        Retrieves the most recent block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, block: Inti) -> str:
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
