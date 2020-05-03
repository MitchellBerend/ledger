from os import environ
import socket
import wallet_interaction_lib


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
    data = client.recv(100).decode("utf-8")
    data = eval(data)
    amount, action = data[0], data[-1]
    print(f"""amount: {amount}\naction: {action}""")
    if action == "check":
        client.send(
            bytes(
                str(wallet_interaction_lib.show_current(**database_login_info)), "utf-8"
            )
        )
        print("check")
        break
    elif action == "withdraw":
        client.send(
            bytes(
                str(
                    wallet_interaction_lib.withdraw_money(amount, **database_login_info)
                ),
                "utf-8",
            )
        )
        print("withdraw")
        break
    elif action == "deposit":
        client.send(
            bytes(
                str(
                    wallet_interaction_lib.deposit_money(amount, **database_login_info)
                ),
                "utf-8",
            )
        )
        print("deposit")
        break
    else:
        client.send(bytes("error", "utf-8"))
        print("error")
        break
    print(data)
