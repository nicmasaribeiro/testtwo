#!/usr/bin/env python3

import asyncio
import threading
import logging
from websockets import serve
from websockets.uri import parse_uri
from websockets.client import connect

# Configure logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class WebSocketServer:
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
			
	async def run_websocket_server(self, host, port):
		async with serve(self.websocket_handler, host, port):
			await asyncio.Future()  # Run forever
			
	def start_server(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.run_websocket_server(self.HOST, self.PORT))
		print(self.messages)
		
def main():
	host = '192.168.1.237'
	base_port = 8000
	num_servers = 10
	
	servers = [WebSocketServer(base_port + i, host) for i in range(num_servers)]
	threads = [threading.Thread(target=server.start_server) for server in servers]
	
	for thread in threads:
		thread.start()
		
	for thread in threads:
		thread.join()
		
if __name__ == '__main__':
	main()
	