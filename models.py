

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
#from flask_socketio import SocketIO, emit
import pandas as pd
from tenacity import retry
from applescript import tell
from geventwebsocket import WebSocketApplication, WebSocketServer
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
from main import db

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