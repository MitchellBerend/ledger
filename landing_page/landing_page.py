import socket
from os import environ
import landing_page_lib


database_login_info = {
    "user": environ["db_user"],
    "password": environ["db_password"],
    "database": "odin",
    "host": socket.gethostbyname("portfolio_db"),
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 5000))
sock.listen(10)
while True:
    client, address = sock.accept()
    symbol = client.recv(10).decode("utf-8")
    if symbol == " ":
        data = landing_page_lib.get_name_price_amount(**database_login_info)
        print(data)
        client.send(bytes(str(data), "utf-8"))
        break
    else:
        print("error")
        client.send(bytes("landing_page error", "utf-8"))
        break
