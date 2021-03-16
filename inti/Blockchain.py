from inti.Inti import Inti
import time


class Blockchain:

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
