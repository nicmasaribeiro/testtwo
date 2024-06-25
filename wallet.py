#!/usr/bin/env python3
from bc import Transaction
import hashlib
from ecdsa import SigningKey, SECP256k1
import binascii as bina
import codecs

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.key_pair = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.key_pair = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.key_pair.verifying_key.to_string().hex()
        
    def sign_transaction(self, transaction):
        if self.public_key != transaction['from_address']:
            raise ValueError('You cannot sign transactions for other wallets!')
        hash_tx = hashlib.sha256((transaction['from_address'] + transaction['to_address'] + str(transaction['amount'])).encode('utf-8')).hexdigest()
        signature = self.key_pair.sign(bytes.fromhex(hash_tx))
        transaction['signature'] = signature.hex()
        
    @staticmethod
    def verify_transaction(transaction):
        public_key = transaction['from_address']
        signature = bytes.fromhex(transaction['signature'])
        hash_tx = hashlib.sha256((transaction['from_address'] + transaction['to_address'] + str(transaction['amount'])).encode('utf-8')).hexdigest()
        verifying_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
        return verifying_key.verify(signature, bytes.fromhex(hash_tx))
    
    def generate_new_address(self):
        new_key_pair = SigningKey.generate(curve=SECP256k1)
        return new_key_pair.verifying_key.to_string().hex()
    
    def get_balance(self, blockchain):
        # Placeholder for balance checking logic. This requires integration with a blockchain.
        # Here, 'blockchain' would be an object that interacts with the blockchain to get balance information.
        pass
        

#n = codecs.encode('hex')
#print(hex(1247783))
#print(n)
##print(n('password')[0])/
#w = Wallet(private_key=codecs.encode(''))#bin.hexlify(' 1247783'.encode()))
#
#w2 = Wallet()
#
#print(w.public_key,'\n',w2.public_key)
#		
### Example of how to use the Wallet class
#if __name__ == "__main__":
#	wallet = Wallet()
#	w2 = Wallet()
#	wallet.public_key
##	transaction = Transaction(wallet.public_key, w2.public_key, 90)
#	transaction = {
#		'from_address': wallet.public_key,
#		'to_address': w2.public_key,
#		'amount': 100
#	}
#	wallet.sign_transaction(transaction)
#	print(transaction)
##	