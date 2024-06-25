from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd
from tenacity import retry
from applescript import tell
import subprocess 
import applescript
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
from flask_socketio import SocketIO, emit
import websockets
from p2p_two import P2PNode
from tornado.httpclient import AsyncHTTPClient
from file_server import handle_client, start_tcp_server
from file_cli import upload_file,download_file
import socket
from wallet import Wallet
from flask_bcrypt import Bcrypt
from bc import Transaction, Block ,Blockchain
from Server import Server
from TCPServer import TCPServer
import sys
from tcp_cli import TCPClient
import datetime as dt

HOST = '0.0.0.0'

# Configure logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

my_msgs = []
socket_ls = [socket.socket() for i in range(100)]
p2p_ls = [P2PNode(socket.gethostname(), i) for i in range(800, 900)]
my_signal = []
TCPserver_ls = [TCPServer(socket.gethostname(), i) for i in range(900, 1000)]
print('Server 0\t',TCPserver_ls[0].host,TCPserver_ls[0].port)
my_server = Server()
tcp = TCPServer(socket.gethostname(), 2020)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class WS(WebSocketApplication):
	def __init__(self, port, host):
		self.signals = []
		self.messages = []
		self.PORT = port
		self.HOST = host
		
	async def websocket_handler(self, websocket, path):
		async for message in websocket:
			logger.info(f"WebSocket received: {message} from {websocket.remote_address}")
			await websocket.send("Hello from server")
			self.signals.append(websocket.remote_address)
			self.messages.append(message)
			return message
		
	async def run_websocket_server(self, host, port):
		async with serve(self.websocket_handler, host, port):
			await asyncio.Future()  # Run forever
		return self.websocket_handler
	
	def start_server(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.run_websocket_server(self.HOST, self.PORT))
		return self.run_websocket_server(self.HOST, self.PORT)
	

def main():
	host = HOST #'192.168.1.14'
	base_port = 8000
	num_servers = 100
	peer2peers = [P2PNode(host, i) for i in range(800, 800+num_servers)]
	servers = [WS(base_port + i, host) for i in range(num_servers)]
	threads = [threading.Thread(target=server.start_server) for server in servers]
	
	for s in servers:
		my_msgs.append(s)
		
	for p in peer2peers:
		my_signal.append(p)
		
	for thread in threads:
		thread.start()
		
	for thread in threads:
		thread.join()
		
		
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	wallet = Wallet()
	
	def __repr__(self):
		return f'<User {self.username}>'
	
class Transport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	host = db.Column(db.String(2048))
	port = db.Column(db.Integer())
	from_address = db.Column(db.String(2048))
	to_address = db.Column(db.String(2048))
	amount = db.Column(db.Float())
	password = db.Column(db.String(60), nullable=False)
	transaction = Transaction(from_address, to_address, amount)
	
	def __repr__(self):
		return f'<User {self.username}>'
	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/signup', methods=['POST','GET'])
def signup():
	if request.method =="POST":
		password = request.values.get("password")
		username = request.values.get("username")
		email = request.values.get("email")
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		new_user = User(username=username, email=email, password=hashed_password,wallet=Wallet())
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'message': 'User created!'}), 201
	return render_template("signup.html")

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == "POST":
		username = request.values.get("username")
		password = request.values.get("password")
		user = User.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			login_user(user)
			return redirect('/users')# jsonify({'message': 'Logged in successfully!'}), 200
		else:
			return redirect('/signup')
	return render_template("login.html")


@app.route('/users', methods=['GET'])
@login_required
def get_users():
	users = User.query.all()
	users_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'publicKey':user.wallet.public_key} for user in users]
	return jsonify(users_list)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
	user = User.query.get_or_404(id)
	return jsonify({'id': user.id, 'username': user.username, 'email': user.email,'publicKey':user.wallet.public_key})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
	data = request.get_json()
	user = User.query.get_or_404(id)
	user.username = data['username']
	user.email = data['email']
	db.session.commit()
	return jsonify({'message': 'User updated!'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
	user = User.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	return jsonify({'message': 'User deleted!'})

@app.route('/')
def start():
	return render_template('index.html')

@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/bs2',methods=['GET','POST'])
@login_required
def bs2():
	if request.method == "POST":			
		value = request.values.get("value")
		addrs_from = request.values.get("from_address")
		addrs_to = request.values.get("to_address")
		webhost = request.values.get("webhost")
		port = request.values.get('port')
		password = request.values.get("password")
		ws_url = f"ws://{webhost}:{port}/?value={value}"
		transaction = Transaction(addrs_from, addrs_to, value)
		data = json.dumps({'address':webhost,'value':value,'ws_url':ws_url,'from_address':addrs_from,'to_address':addrs_to})
		new_transport = Transport(port=port,host=webhost,password=password,from_address=addrs_from,to_address=addrs_to)
		db.session.add(new_transport)
		db.session.commit()
		return  data
	return render_template("bs2.html")

@app.route('/transact',methods=['GET','POST'])
@login_required
def transact():
	if request.method == "POST":
		username_from = request.values.get("username_from")
		username_to = request.values.get("username_to")
		
		value = request.values.get("value")
		from_addrs = request.values.get("from_address")
		to_addrs = request.values.get("to_address")
		user = User.query.get_or_404(username_from)
		user2 = User.query.get_or_404(username_to)
		transaction = {'from_address': user.wallet.public_key,'to_address': user2.wallet.public_key,'amount': 100}
		user.wallet.sign_transaction(transaction)
		
		data = json.dumps({'from_addrs':from_addrs,'value':value,'to_addrs':to_addrs})
		return  data #render_template("bs2.html")
	return render_template("trans.html")

@app.route('/get/transports',methods=['GET'])
@login_required
def get_transport():
	transports = Transport.query.all()
	transports_list = [{'id': t.id, 'host': t.host, 'port': t.port, 'from_address':t.from_address} for t in transports]
	return jsonify(transports_list)

@app.route('/tcp/<host>/<int:port>')
@login_required
def start_tcp(host,port):
	tcp = TCPServer(host, port)
	tcp.start()
	return "Success"

@app.route('/tcp/<host>/<int:port>')
@login_required
def get_tcp(host,port):
#	loop = asyncio.get_running_loop()
	tcp = TCPServer(host, port)
	tcp.start()
#	loop.run_until_complete()
	return "Success"

@app.route('/connect-tcp/<host>/<int:port>')
@login_required
def start_connect(host,port):
	tcp = TCPClient(host, port)
	tcp.client_program()
	return "Success"


@app.route('/tcpcli')
def external_terminal_tcp_server():
	try:
#		subprocess.check_output(['python3','tcp_cli.py'])
		#	from applescript import tell
		cmd = '''	
			tell application "Terminal"
					activate
					do script "cd ./Desktop/project
					python3 tcp_cli.py"
			end tell'''
		tell.app("Terminal", cmd)
	except ValueError:
		pass
	finally:
		return "Success"
	
@app.route('/sock')
def sock():
	return render_template('test-one.html')

@socketio.on('connect')
def connection():
	emit('connected')
	
##########################
# Usage Still Considering
##########################
	
@app.route('/wss/<endpoint>')
def websocket(endpoint):
	i = int(endpoint)
	p2p_ls[i].listen_to_peer(socket.socket())
#	con,addrs = web.accept()
	return "Success"#render_template("ws1.html")#redirect(url)

#@app.route('/ws2')
#def ws2():
#	if request.method == "POST":
#		ws = WS(endpoint, '0.0.0.0')
#		url = str("ws://"+endpoint+'/')
#		print(url)
#	return render_template("ws1.html",end=5000)#redirect(url)

@app.route('/ws2/<endpoint>')
def ws2(endpoint):
	if request.method == "POST":
		ws = WS(endpoint, '0.0.0.0')
		url = str("ws://"+endpoint+'/')
		print(url)
	return render_template("ws1.html",end=endpoint)

@app.route('/msg-connect')
def msg():
	for i in range(len(my_msgs)):
		try:
			my_msgs[i].start_server()
			
		except:
			pass
		finally:
			return "Success" #[my_msgs[i].messages for i in range(len(my_msgs))]
		
		
##################
# Download Files 
##################
@app.route('/download')
def dlink():
	return render_template("download.html")

@app.route('/download/<name>/<host>/<int:port>')
async def download(host,port,name):
	try:
		await download_file(name, port, host)
	except OSError:
		pass
	finally:
		return "Success"
	
@app.route('/cli/<host>/<int:port>')
async def cli(host,port):
	loop = asyncio.get_running_loop()
	try:
		loop.run_until_complete(start_tcp_server(host, port)) 
		
	except OSError:
		pass
	return "Success"

##################
# Upload Files 
##################

@app.route('/upload')
def ulink():
	return render_template("upload.html")

@app.route('/upload/<name>/<host>/<int:port>')
async def upload(host,port,name):
	try:
		await upload_file(name, port, host)
	except OSError:
		pass
	finally:
		return "Success"
	
	
def run_sock():
	return socketio.run(app)

def run():
	return app.run(host='192.168.1.237',port=8080)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		
	server_thread = threading.Thread(target=my_server.run)
	tcp_thread = threading.Thread(target=tcp.server_program)
	app_thread = threading.Thread(target=run)
	main_thread = threading.Thread(target=main)
	sock_thread = threading.Thread(target=run_sock)
	
	server_thread.start()
	app_thread.start()
#	main_thread.start()
#	tcp_thread.start()
	
#	server_thread.join()
	app_thread.join()
#	main_thread.join()
#	sock_thread.join()
#	tcp_thread.join()