from wallet import Wallet
import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Crypto.PublicKey import RSA

class Client():
	def __init__(self):
		self.pending_peers = []
		self.wallet = Wallet()
		self.network_address = {'webhost':[],'signature':[],"key":[]}
		self.receipts = []
		self.private_key_pass = b'1247783'
	
	def create_genisis():
		self.network_address['webhost'].append(socket.gethostname())
		self.network_address['signature'].append(self.wallet.generate_new_address())
		self.network_address['key'].append(self.get_new_key(''))
		
	def get_new_key(self):
		private_key = rsa.generate_private_key(public_exponent=3, key_size=2048)#RSA.generate()
		private_key_pass = self.private_key_pass #b"1247783"
		encrypted_pem_private_key = private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.BestAvailableEncryption(private_key_pass))
		return encrypted_pem_private_key
	
	def p2p_token(self):
		return RSA.generate(3072)
	
	def handshake(self,port):
		sock = socket.socket()
		sock.connect((socket.gethostname(),port))
		sock.sendall(b"Send Intraweb Address")
		return sock.recv(2048)
	
	def decrypt(self):
		unencrypted_pem_private_key = self.private_key_pass.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.TraditionalOpenSSL,
			encryption_algorithm=serialization.NoEncryption())
		return unencrypted_pem_private_key
