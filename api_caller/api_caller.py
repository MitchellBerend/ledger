import requests as r
import mysql.connector as sql
import socket
from os import environ
import api_caller_lib


database_login_info = {
    "user": environ["db_user"],
    "password": environ["db_password"],
    "database": "cache",
    "host": socket.gethostbyname("portfolio-db"),
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 5000))
sock.listen(10)
while True:
    client, address = sock.accept()
    symbol = client.recv(10).decode("utf-8").upper()
    print(symbol)
    data = api_caller_lib.get_data_alphavantage(
        symbol
    )
    api_caller_lib.add_to_db(data, **database_login_info)
    print(data)
    client.send(bytes(str(data), "utf-8"))
    print(f"Sending data to {address}.")
    break
