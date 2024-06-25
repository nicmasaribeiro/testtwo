#!/usr/bin/env python3

#!/usr/bin/env python3

import socket
import sys

HOST = "192.168.1.14"  # Server's hostname or IP address
PORT = 5050            # Server's port

def upload_file(filename,port,host):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		s.sendall(f"UPLOAD {filename}".encode())
		with open(filename, 'rb') as f:
			while chunk := f.read(1024):
				s.sendall(chunk)
		s.sendall(b"UPLOAD COMPLETE")
		response = s.recv(1024).decode()
		print(f"Server response: {response}")
		
def download_file(filename,port,host):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		s.sendall(f"DOWNLOAD {filename}".encode())
		with open(f"downloaded_{filename}", 'wb') as f:
			while True:
				chunk = s.recv(1024)
				if chunk == b"DOWNLOAD COMPLETE":
					break
				f.write(chunk)
		print(f"Downloaded {filename}")
		
#if __name__ == "__main__":
#	upload_file('main.py', 9090, '0.0.0.0')
##	if len(sys.argv) != 3:
##		print("Usage: python file_client.py <UPLOAD/DOWNLOAD> <filename>")
##		sys.exit(1)
#	cmd = input("command ==>\t").upper()
#	name = input("filename ==>\t").upper()
##	command, filename = sys.argv[1], sys.argv[2]
#	if cmd == "UPLOAD":
#		upload_file(name)
#	elif cmd == "DOWNLOAD":
#		download_file(name)
#	else:
#		print("Invalid command")
		