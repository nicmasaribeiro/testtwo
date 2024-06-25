
import socket

class TCPClient:
	def __init__(self,host,port):
		self.host = host #"192.168.1.237"#socket.gethostname()  # or use the server's IP address
		self.port = port #8000  # the same port as used by the server
		
	def client_program(self):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
		client_socket.connect((self.host, self.port))  # connect to the server
		
		message = input(" -> ")  # take input
		
		while message.lower().strip() != 'bye':
			client_socket.send(message.encode())  # send message
			data = client_socket.recv(1024).decode()  # receive response
			
			print(f"Received from server: {data}")  # show in terminal
			
			message = input(" -> ")  # again take input
			
		client_socket.close()  # close the connection
		
		
if __name__ == "__main__":
	tcp_client = TCPClient('0.0.0.0', 9091)
	tcp_client.client_program()
#	