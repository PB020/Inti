from flask import Flask, request
import requests

from inti import Blockchain
from inti import Inti
import json
import time

# Initialize flask application
app = Flask(__name__)

# Initialize a blockchain object
blockchain = Blockchain.Blockchain()

# Contains the host addresses of other participating members of the network
peers = set()


@app.route('/new_transaction', methods=['POST'])
def new_transaction() -> tuple:
    """
    Endpoint to submit a new transaction
    """
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


@app.route('/chain', methods=['GET'])
def get_chain() -> str:
    """
    Endpoint to query all of the data to display
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data), "chain": chain_data})


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions() -> str:
    """
    Endpoint to mine unconfirmed transactions
    """
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined".format(result)


@app.route('/pending_tx')
def get_pending_tx() -> str:
    """
    Endpoint to get unconfirmed transactions on the blockchain
    """
    return json.dumps(blockchain.unconfirmed_transactions)


@app.route('/register_node', methods=['POST'])
def register_new_peers() -> str:
    """
    Endpoint to add new peers to the network
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    peers.add(node_address)

    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node() -> tuple:
    """
    Internally calls the 'register_node' endpoint to register current node
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content Type': "application/json"}

    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers

        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        return response.content, response.status_code


def create_chain_from_dump(chain_dump: str) -> Blockchain.Blockchain:
    blockchain = Blockchain()
    for idx, block_data in enumerate(chain_dump):
        block = Inti.Inti(block_data["index"],
                          block_data["transactions"],
                          block_data["timestamp"],
                          block_data["previous_hash"])
        proof = block_data['hash']

        if idx > 0:
            added = blockchain.add_block(block, proof)
            if not added:
                raise Exception("The chain dump is tampered!")
        else:
            blockchain.chain.append(block)
    return blockchain


@app.route('/add_block', methods=['POST'])
def verify_and_add_block() -> tuple:
    """
    Endpoint to add a block mined by someone else to the node's chain
    """
    block_data = request.get_json()
    block = Inti.Inti(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"])
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


def announce_new_block(block: Inti.Inti) -> None:
    """
    Announces to the network once a block has been mined
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))


def consensus() -> bool:
    """
    Consensus algorithm: if a longer valid chain is found, the chain is replaced
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']

        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False
