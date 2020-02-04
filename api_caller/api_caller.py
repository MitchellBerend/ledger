import requests as r
import mysql.connector as sql
import socket
from os import environ
import lib


"""
NOTES
Receives symbol,
checks cache,
if in cache -> get from cache, send back
if not in cache -> make api call

api_key = environ["api_caller"]

database info = {
    "user":"api_caller",
    "password":environ["db_password"],
    "database":"cache"
}

timestamp varchar(20),open float,high float,low float,close float,volume int,symbol varchar(4),id varchar(56)

"""

database_login_info = {
    "user":"root",
    "password":environ["db_password"],
    "database":"cache",
    "host":socket.gethostbyname("portfolio-db")
}

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((socket.gethostname(),5000))
sock.listen(10)
while True:
    client, address = sock.accept()
    symbol = client.recv(10).decode("utf-8").upper()
    print(symbol)
    data = lib.get_data_alphavantage(symbol,environ["api_caller"]) # make alphavatnage api call
    if data == None:
        print(data)
        data = lib.format_data(lib.retrieve_data(symbol,**database_login_info))
        print("data from cache")
        client.send(bytes(str(data),"utf-8"))
        print(data)
        print("none")
        break
    else:
        lib.add_to_db(data,**database_login_info)
        client.send(bytes(str(data),"utf-8"))
        print(data)
        break
    print(f"Sending data to {address}.")