#!/usr/bin/env python3
from ws_class import main
from flask import Flask, render_template
import asyncio
import threading 
import functools
import websockets
from websockets.server import serve


async def hello():
	uri = "ws://192.168.1.177:808"
	async with websockets.connect(uri) as websocket:
		await websocket.send("Hello")
		response = await websocket.recv()
		print(f"WebSocket received: {response}")
		return response

async def run():
	uri = "ws://192.168.1.14:5050"
	with websockets.connect(uri) as ws:
		await ws.send("hi")

async def ws_handler(websocket, path, context):
	await websocket.send("Count={}".format(context.current_count))
	
some_data = "data"
	
bound_handler = functools.partial(ws_handler, context=some_data)

start_server = websockets.serve(bound_handler, '192.168.1.14', 8765)

	
	
	
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("basic-script.html")


if __name__ =="__main__":
	app_th = threading.Thread(target=app.run)
#	app_th.start()
	server_th = threading.Thread(target=start_server)
#	server_th.start()
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()