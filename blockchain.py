import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

def mh_hash_transaction(mh_transaction):
    """Hashuje pojedynczą transakcję."""
    mh_transaction_string = json.dumps(mh_transaction, sort_keys=True).encode()
    return hashlib.sha256(mh_transaction_string).hexdigest()

def mh_create_merkle_root(mh_transactions):
    """Tworzy korzeń drzewa Merkle dla listy transakcji."""
    if len(mh_transactions) == 0:
        return None

    mh_hashed_transactions = [mh_hash_transaction(tx) for tx in mh_transactions]

    while len(mh_hashed_transactions) > 1:
        if len(mh_hashed_transactions) % 2 != 0:
            mh_hashed_transactions.append(mh_hashed_transactions[-1])  # Duplikujemy ostatni hash

        new_level = []
        for i in range(0, len(mh_hashed_transactions), 2):
            mh_combined = mh_hashed_transactions[i] + mh_hashed_transactions[i + 1]
            mh_combined_hash = hashlib.sha256(mh_combined.encode()).hexdigest()
            new_level.append(mh_combined_hash)

        mh_hashed_transactions = new_level

    return mh_hashed_transactions[0]

class Blockchain(object):
    def __init__(self):
        self.mh_chain = []
        self.mh_current_transactions = []
        self.mh_mempool = []

        # Tworzenie bloku genesis
        self.mh_new_block(mh_proof=100, mh_previous_hash='1')
    def mh_is_chain_valid(self):
        """Sprawdza poprawność całego łańcucha bloków."""
        chain = self.mh_chain

        for i in range(1, len(chain)):
            prev_block = chain[i - 1]
            curr_block = chain[i]

            # Sprawdź hash poprzedniego bloku
            if curr_block['mh_previous_hash'] != self.mh_hash(prev_block):
                return False, f"Błąd hasha między blokiem {i} a {i + 1}"

            # Sprawdź poprawność proof-of-work
            if not self.mh_valid_proof(prev_block['mh_proof'], curr_block['mh_proof']):
                return False, f"Niepoprawny proof-of-work w bloku {i + 1}"

        return True, "Łańcuch jest poprawny"


    def mh_new_block(self, mh_proof, mh_previous_hash=None):
        mh_merkle_root = mh_create_merkle_root(self.mh_current_transactions)
        mh_block = {
            'mh_index': len(self.mh_chain) + 1,
            'mh_timestamp': time(),
            'mh_transactions': self.mh_current_transactions,
            'mh_proof': mh_proof,
            'mh_previous_hash': mh_previous_hash or self.mh_hash(self.mh_chain[-1]),
            'mh_merkle_root': mh_merkle_root
        }
        self.mh_current_transactions = []
        self.mh_chain.append(mh_block)
        return mh_block

    def mh_new_transaction(self, mh_sender, mh_receiver, mh_amount):
        self.mh_current_transactions.append({
            'mh_sender': mh_sender,
            'mh_receiver': mh_receiver,
            'mh_amount': mh_amount
        })
        return self.mh_last_block['mh_index'] + 1

    def mh_add_transaction_to_mempool(self, mh_sender, mh_receiver, mh_amount):
        mh_transaction = {
            'mh_sender': mh_sender,
            'mh_receiver': mh_receiver,
            'mh_amount': mh_amount,
        }
        self.mh_mempool.append(mh_transaction)
        return len(self.mh_mempool)

    def mh_proof_of_work(self, mh_last_proof):
        mh_proof = 0
        while not self.mh_valid_proof(mh_last_proof, mh_proof):
            mh_proof += 1
        return mh_proof

    def mh_valid_proof(self, mh_last_proof, mh_proof):
        mh_guess = f'{mh_last_proof}{mh_proof}'.encode()
        mh_guess_hash = hashlib.sha256(mh_guess).hexdigest()
        return mh_guess_hash.endswith("11")

    @staticmethod
    def mh_hash(mh_block):
        mh_block_string = json.dumps(mh_block, sort_keys=True).encode()
        return hashlib.sha256(mh_block_string).hexdigest()

    @property
    def mh_last_block(self):
        return self.mh_chain[-1]

# Flask app
app = Flask(__name__)
mh_node_identifier = str(uuid4()).replace('-', '')
mh_blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mh_mine():
    mh_last_block = mh_blockchain.mh_last_block
    mh_last_proof = mh_last_block['mh_proof']
    mh_proof = mh_blockchain.mh_proof_of_work(mh_last_proof)

    mh_blockchain.mh_new_transaction(
        mh_sender="0",
        mh_receiver=mh_node_identifier,
        mh_amount=1,
    )

    mh_previous_hash = mh_blockchain.mh_hash(mh_last_block)
    mh_block = mh_blockchain.mh_new_block(mh_proof, mh_previous_hash)

    response = {
        'message': 'New Block Mined',
        'index': mh_block['mh_index'],
        'transactions': mh_block['mh_transactions'],
        'proof': mh_block['mh_proof'],
        'previous_hash': mh_block['mh_previous_hash'],
        'merkle_root': mh_block['mh_merkle_root'],
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def mh_new_transaction():
    mh_values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in mh_values for k in required):
        return 'Missing values', 400
    mh_index = mh_blockchain.mh_new_transaction(
        mh_values['sender'], mh_values['recipient'], mh_values['amount']
    )
    return jsonify({'message': f'Transaction will be added to Block {mh_index}'}), 201

@app.route('/chain', methods=['GET'])
def mh_full_chain():
    response = {
        'chain': mh_blockchain.mh_chain,
        'length': len(mh_blockchain.mh_chain),
    }
    return jsonify(response), 200

@app.route('/validate', methods=['GET'])
def mh_validate_chain():
    is_valid, message = mh_blockchain.mh_is_chain_valid()
    response = {
        'valid': is_valid,
        'message': message,
        'length': len(mh_blockchain.mh_chain)
    }
    return jsonify(response), 200 if is_valid else 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
