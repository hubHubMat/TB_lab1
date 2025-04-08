import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.mh_chain = []
        self.mh_current_transactions = []

        self.mh_new_block(mh_previous_hash="Matlak", mh_proof=57185)
    def mh_new_block(self, mh_proof, mh_previous_hash=None):
        mh_block = {
            'mh_index': len(self.mh_chain) + 1,
            'mh_timestamp': time(),
            'mh_transactions': self.mh_current_transactions,
            'mh_proof': mh_proof,
            'mh_previous_hash': mh_previous_hash or self.mh_hash(self.mh_chain[-1])
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
        return self.mh_last_block['index'] + 1

    def mh_proof_of_work(self, mh_last_proof):
        mh_proof = 0
        while self.mh_valid_proof(mh_last_proof, mh_proof) is False:
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

if __name__ == '__main__':
    blockchain = Blockchain()
    mh_last_proof = blockchain.mh_last_block['mh_proof']
    print("Szukanie dowodu pracy...")
    mh_proof = blockchain.mh_proof_of_work(mh_last_proof)
    mh_block = blockchain.mh_new_block(mh_proof)

    print("Nowy blok dodany:")
    print(json.dumps(mh_block, indent=4))