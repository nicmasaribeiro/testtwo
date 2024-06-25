#!/usr/bin/env python3

#!/usr/bin/env python3

import socket
import threading

HOST = "192.168.0.183"  # Listen on all network interfaces
PORT = 5050       # Port for the TCP server

def handle_client(conn, addr):
	print(f"Connected by {addr}")
	while True:
		data = conn.recv(1024).decode()
		if not data:
			break
		command, filename = data.split()
		if command == "UPLOAD":
			with open(filename, 'wb') as f:
				while True:
					chunk = conn.recv(1024)
					if not chunk:
						break
					f.write(chunk)
				conn.sendall(b"UPLOAD COMPLETE")
		elif command == "DOWNLOAD":
			try:
				with open(filename, 'rb') as f:
					while True:
						chunk = f.read(1024)
						if not chunk:
							break
						conn.sendall(chunk)
				conn.sendall(b"DOWNLOAD COMPLETE")
			except FileNotFoundError:
				conn.sendall(b"FILE NOT FOUND")
	conn.close()
	
def start_tcp_server(host,port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((host, port))
		server_socket.listen()
		print(f"TCP server listening on {host}:{port}")
		while True:
			conn, addr = server_socket.accept()
			threading.Thread(target=handle_client, args=(conn, addr)).start()
#			
#if __name__ == "__main__":
#	start_tcp_server(HOST,PORT)
	