
import datetime
from flask import Flask, jsonify, request
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse
# 1. create blockchain class


class Blockchain():
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(prev_hash='0', proof=1)
        self.nodes = set()

    def create_block(self, prev_hash, proof):
        block = {'timestamp': str(datetime.datetime.now()),
                 'prev_hash': prev_hash,
                 'proof': proof,
                 'index': len(self.chain)+1,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def get_proof(self, prev_proof):
        #prev_proof = self.get_prev_block['proof']
        found = False
        proof = 1
        while(not found):
            # any non symmetric function with fair enough complexity
            hash_found = hashlib.sha256(
                str(proof**2-prev_proof**2).encode()).hexdigest()
            if(hash_found[:4] == '0000'):
                found = True
            else:
                proof = proof+1
        return proof

    def hash(self, block):
        # convert to json and sort to keys to get uniform hashing
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def sanity_check(self):
        # 2 checks needed
        # 1. prev hash matches with current hash stored
        prev = self.chain[0]
        index = 1
        while(index < len(self.chain)):
            prev_hash = self.chain[index]['prev_hash']
            if(prev_hash != self.hash(prev)):
                return False
            # 2. proof of work is correct
            proof = self.chain[index]['proof']
            prev_proof = prev['proof']
            hash_found = hashlib.sha256(
                str(proof**2-prev_proof**2).encode()).hexdigest()
            if(hash_found[:4] != '0000'):
                found = False
            prev = self.chain[index]
            index += 1
        return True
    # transactions to make it cryptocurrency

    def add_transaction(self, amount, sender, receiver):
        self.transactions.append(
            {'sender': sender, 'receiver': receiver, 'amount': amount})
        prev_block = self.get_prev_block()
        return prev_block['index']+1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    # consesus to make all nodes have same chain

    def replace_nodes(self):
        network = self.nodes
        longest_chain = None
        max_len = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/list_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_len and self.sanity_check(chain):
                    max_len = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# 2. Actual working and mining
blockchain = Blockchain()
# Webapp
app = Flask(__name__)
# Create node addresses
node_addresses = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    prev_block = blockchain.get_prev_block()
    proof = blockchain.get_proof(prev_block['proof'])
    block = blockchain.create_block(blockchain.hash(prev_block), proof)
    blockchain.add_transaction(
        sender=node_addresses, receiver='Bob', amount=10)
    response = {'message': ' You did it! New block created',
                'index': block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'], 'prev_hash': block['prev_hash'], 'transactions': block['transactions']}
    return jsonify(response), 200


@app.route('/list_chain', methods=['GET'])
def list_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/sanity', methods=['GET'])
def sanity():
    valid = blockchain.sanity_check()
    if(valid):
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'Sorry. Something went wrong!'}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = {'sender', 'receiver', 'amount'}
    if not all(key in json for key in transaction_keys):
        return 'Missing keys', 400
    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount'])
    response = {'message': f'Transaction will be added to {index}'}
    return response, 201
# 3. decentralizing blockchain

# Create new nodes


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node found', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All nodes added successfully. Chain contains following nodes',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replace all chains with most recent one


@app.route('/update_chain', methods=['GET'])
def update_chain():
    is_chain_replaced = blockchain.update_chain()
    if(is_chain_replaced):
        response = {
            'message': 'Nodes had different chians. Hence, Chain is replaced', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'Chain is already updated',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5003)
