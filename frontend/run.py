from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import socket
from time import sleep
from os import system
from multiprocessing import Process

app = Flask(__name__)

api = Api(app)

@app.route('/')
def index():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname("landing_page"),5000))
    sock.send(bytes(" ", "utf-8"))
    data = ""
    while True:
        msg = sock.recv(1024)
        if len(msg) <= 0:
            break
        data += msg.decode("utf-8")
    data = eval(data)
    return jsonify(data)


class symbol_data(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", required=True)
        args = parser.parse_args()
        print(args)
        symbol = args["symbol"]
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((socket.gethostbyname("api_caller"),5000))
        sock.send(bytes(symbol, "utf-8"))
        data = ''
        while True:
            msg = sock.recv(1024)
            if len(msg) <= 0:
                break
            data += msg.decode("utf-8")
        try:
            data = eval(data)
        except:
            return "no data available"
        return jsonify(data)

class tracker(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", required=True)
        parser.add_argument("amount", required=True)
        args = parser.parse_args()
        data = [args["symbol"], args["amount"], "post"]
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((socket.gethostbyname("track_handler"),5000))
        sock.send(bytes(str(data), "utf-8"))
        data = ""
        while True:
            msg = sock.recv(1024)
            if len(msg) <= 0:
                break
            data += msg.decode("utf-8")
        return data

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", required=True)
        args = parser.parse_args()
        symbol = args["symbol"]
        data = [symbol, "delete"]
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((socket.gethostbyname("track_handler"),5000))
        sock.send(bytes(str(data), "utf-8"))
        data = ""
        while True:
            msg = sock.recv(1024)
            if len(msg) <= 0:
                break
            data += msg.decode("utf-8")
        return data


api.add_resource(symbol_data, '/symbol_data')
api.add_resource(tracker, '/tracker')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")