#!/usr/bin/env python3

import threading
import socket

class TCPServer(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		
	def run(self):
		self.server_program()
		
	def server_program(self):
		# create a socket object
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# reuse the address
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# bind the socket to the address and port
		server_socket.bind((self.host, self.port))
		
		# listen for incoming connections
		server_socket.listen(100)
		print(f"Server listening on {self.host}:{self.port}")
		
		conn, address = server_socket.accept()  # accept new connection
		print(f"Connection from: {address}")
		
		while True:
			# receive data stream. it won't accept data packet greater than 1024 bytes
			data = conn.recv(1024).decode()
			if not data:
				# if data is not received, break
				break
			print("Received from client: " + str(data))
			data = input(' -> ')
			conn.send(data.encode())  # send data to the client
			
		conn.close()  # close the connection
		
tcp = TCPServer('0.0.0.0', 9091)
tcp.start()