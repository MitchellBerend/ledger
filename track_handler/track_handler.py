import socket
import track_handler_lib
from os import environ

database_login_info = {
    "user": environ["db_user"],
    "password": environ["db_password"],
    "database": "profile",
    "host": socket.gethostbyname("profile_odin"),
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 5000))
sock.listen(10)
while True:
    client, address = sock.accept()
    data = client.recv(100).decode("utf-8")
    data = eval(data)
    if track_handler_lib.request_checker(data) == "delete":
        symbol = data[0].upper()
        check = track_handler_lib.check_profile_for_existing_data(
            data[0], **database_login_info
        )
        if check == True:
            track_handler_lib.add_wallet(symbol, **database_login_info)
            track_handler_lib.delete_data_from_profile(symbol, **database_login_info)
            client.send(bytes(f"""{symbol} deleted from the tracker.""", "utf-8"))
            break
        else:
            client.send(bytes("Entry does not exist.", "utf-8"))
            break
    elif track_handler_lib.request_checker(data) == "post":
        symbol = data[0].upper()
        amount = float(data[1])
        close = track_handler_lib.make_api_request(symbol)
        total = close * amount
        track_handler_lib.subtract_wallet(symbol, total, **database_login_info)
        track_handler_lib.insert_data_in_profile(
            symbol, close, amount, **database_login_info
        )
        client.send(
            bytes(
                f"""symbol: {symbol}, value: {close}, amount: {amount}, total: {total}""",
                "utf-8",
            )
        )
        break
    print(data)
    print(f"Sending data to {address}.")















