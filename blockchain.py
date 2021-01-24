
import datetime
from flask import Flask, jsonify
import hashlib
import json
# create blockchain class


class Blockchain():
    def __init__(self):
        self.chain = []
        self.create_block(prev_hash='0', proof=1)

    def create_block(self, prev_hash, proof):
        block = {'timestamp': str(datetime.datetime.now()),
                 'prev_hash': prev_hash,
                 'proof': proof,
                 'index': len(self.chain)+1}
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


blockchain = Blockchain()
app = Flask(__name__)


@app.route('/mine', methods=['GET'])
def mine():
    prev_block = blockchain.get_prev_block()
    proof = blockchain.get_proof(prev_block['proof'])
    block = blockchain.create_block(blockchain.hash(prev_block), proof)
    response = {'message': ' You did it! New block created',
                'index': block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'], 'prev_hash': block['prev_hash']}
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


app.run(host='0.0.0.0', port=5000)
