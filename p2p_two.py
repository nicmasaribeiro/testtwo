import socket
import threading
import random
import json
import Client

class P2PNode():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.stream = []

    def start_server(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
    
    def activate_peer_communication(self,port):
        host = socket.gethostname()
        port = port #random.randint(700, 800)  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host 
        server_socket.listen(100)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            self.stream.append(data)
            if not data:
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # send data to the client
        conn.close()  # close the connection
        return conn,address
    
    
    def activate_peer_handshake(self,port,cli):
        token = cli.p2p_token()
        host = socket.gethostname()
        port = port 
        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host 
        server_socket.listen(100)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        blob = {'remote_address':address,'connection':conn,'token':token}
        self.stream.append(blob)
        data = json.dumps(blob)
        conn.send(data.encode())
        return conn,address,data

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received: {message}")
                    self.broadcast(message)
                else:
                    break
            except:
                break
        client_socket.close()

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, peer_port))
        self.peers.append(peer_socket)
        listen_thread = threading.Thread(target=self.listen_to_peer, args=(peer_socket,))
        listen_thread.start()
        return peer_socket.listen(888)

    def listen_to_peer(self, peer_socket):
        while True:
            try:
                message = peer_socket.recv(1024).decode()
                if message:
                    print(f"Received from peer: {message}")
                else:
                    break
            except:
                break
        peer_socket.close()

    def broadcast(self, message):
        for peer_socket in self.peers:
            try:
                peer_socket.sendall(message.encode())
            except:
                self.peers.remove(peer_socket)

    def send_message(self, message):
        self.broadcast(message)
        

#node = P2P('0.0.0.0', 0)

#if __name__ == "__main__":
#   host = socket.gethostname()
#   print(host)
#   port = 3030
#   node = P2PNode(host, 5050)
#   sock_ls = [socket.socket()]
##   node.start_server()
#   
#   node_th = threading.Thread(target=node.start_server)
#   p2p_th = threading.Thread(target=node.connect_to_peer,args=(host,5051))
#   p2p_listen_th = threading.Thread(target=node.listen_to_peer,args=(sock_ls))
#   p2p_broadcast_th = threading.Thread(target=node.broadcast,args=(['hello']))
#   
#   node_th.start()
#   p2p_th.start()
#   p2p_listen_th.start()
#   p2p_broadcast_th.start()
#   
#   node_th.join()
#   p2p_th.join()
#   p2p_listen_th.join()
#   p2p_broadcast_th.join()
##   node.connect_to_peer(host, 8097)
##   # Example to connect to another peer
##   peer_host = "192.168.1.237"
##   peer_port = 3030
##   node.connect_to_peer(peer_host, peer_port)
##
#   while True:
#       message = input("Enter message to broadcast: ")
#       node.send_message(message)
    