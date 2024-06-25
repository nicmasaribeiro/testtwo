from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import ssl
import json
from flask import Flask,render_template,session,request,redirect
from flask_sqlalchemy import SQLAlchemy
import asyncio
import threading
import logging
from websockets import serve
from websockets.uri import parse_uri
from websockets.client import connect
import socket
from flask_socketio import SocketIO
import websockets
from p2p_two import P2PNode
from tornado.httpclient import AsyncHTTPClient
from file_server import handle_client, start_tcp_server
from file_cli import upload_file,download_file
import socket
from wallet import Wallet
from flask_bcrypt import Bcrypt
from bc import Transaction, Block ,Blockchain
import datetime as dt
from requests import get, Request

class Server():
	super(Request)
	def __init__(self,HOST):
		self.HOST = HOST
		self.event = threading.Event()
	
	def listen(self,index,servers_ls):
		channel = servers_ls[index]
		channel.listen(8)
		
	def activate_chain(self,start,stop):
		servers = [self.create_address(i) for i in range(start, stop)]
		return servers
	
	def create_address(self, port):
		s = socket.socket()
		s.bind((self.HOST,port))
		address = socket.create_connection((self.HOST,port))
		return address
			
	def start(self,start,stop):
		thread = threading.Thread(target=self.activate_chain,args=(start,stop))
		thread.start()
		thread.join()

	
	def run(self):
		server = '192.168.1.237'#'137.184.226.245'
		ssh_port = 2020
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock.bind((server, ssh_port))
			sock.listen(100)
			print('[+] Listening for connection ...')
			client, addr = sock.accept()
			while True:
				data = input("==>\t")
				client.send(data.encode())
		except Exception as e:
			print('[-] Listen failed: ' + str(e))
			sys.exit(1)
		else:
			print(f'[+] Got a connection! from {addr}')

#s = Server('0.0.0.0')
#s.start(10,20)

#servers_ls = s.activate_chain(10,20)

#server =  s.listen(0, servers_ls)
#print(s.chain)
#print('here is connected',s.create_address(80))
#print(s.is_chain_valid())
#print(s.chain)
##s.start()