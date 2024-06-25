import threading
import websockets
from flask_socketio import SocketIO
from flask import Flask

class WS(Flask):
	def __init__(self, port, host):
		self.signals = []
		self.messages = []
		self.PORT = port
		self.HOST = host
		self.app = Flask(__doc__)
		self.permanent_websocket = SocketIO(self.app)
	
		
	async def websocket_handler(self, websocket, path):
		async for message in websocket:
			logger.info(f"WebSocket received: {message} from {websocket.remote_address}")
			await websocket.send("Hello from server")
			self.signals.append(websocket.remote_address)
			self.messages.append(message)
			return message
			#my_signal.append(websocket.remote_address)
			#my_msgs.append(message)
			
	async def run_websocket_server(self, host, port):
		async with serve(self.websocket_handler, host, port):
			await asyncio.Future()  # Run forever
		return self.websocket_handler
			
	def start_server(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.run_websocket_server(self.HOST, self.PORT))
		return self.run_websocket_server(self.HOST, self.PORT)
	
	async def hello():
		uri = "ws://192.168.1.14:8020/"
		async with websockets.connect(uri) as websocket:
			await websocket.send("Hello")
			response = await websocket.recv()
			print(f"WebSocket received: {response}")