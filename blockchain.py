# http client: Postman
# pip install Flask
# imports

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 : Building a Blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash='0')

    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while(not check_proof):
            hash_operation = hashlib.sha256(
                str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if(hash_operation[:4] == '0000'):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def sanity_check(self, chain):
        prev = chain[0]
        index = 1
        while(index < len(chain)):
            block = chain[index]
            if(block['prev_hash'] != self.hash(prev)):
                return False
            prev_proof = pre['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if(hash_operation[:4] != '0000'):
                return false
            prev = block
            index += 1
        return True

# Part 2 : Mining the Blockchain


# Create Web App
app = Flask(__name__)
blockchain = Blockchain()

# Mining a Block


@app.route('/mineblock', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {'message': 'Congratulations, Mining successful!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    return jsonify(response), 200
# Get full blockchain


@app.route('/getchain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200


# Runnig the App
app.run(host='0.0.0.0', port=5000)
