import socket
import lib
from os import environ
#   decide wheter the request is a put or delete request

#   put     -> make api request 
#   delete  -> delete entry from profile database

#   put     -> send symbol to api caller, get the latest data, insert into db

#   delete  -> verify data in db, delete entry

#   return performed action result.

database_login_info = {
    "user":"root",
    "password":environ["db_password"],
    "database":"profile",
    "host":socket.gethostbyname("profile_odin")
}

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((socket.gethostname(),5000))
sock.listen(10)
while True:
    client, address = sock.accept()
    data = client.recv(100).decode("utf-8")
    data = eval(data)
    if lib.request_checker(data) == "delete":
        check = lib.check_profile_for_existing_data(data[0],**database_login_info)
        if check == True:
            lib.delete_data_from_profile(data[0],**database_login_info)
            client.send(bytes(f"""{data[0]} deleted from the tracker.""","utf-8"))
            break
        else:
            client.send(bytes("Entry does not exist.","utf-8"))
            break
    elif lib.request_checker(data) == "post":
        close = lib.make_api_request(data[0])
        lib.insert_data_in_profile(data[0],close,data[1],**database_login_info)
        client.send(bytes(f"""symbol: {data[0]}, value: {close}, amount: {data[1]}, total: {close*float(data[1])}""","utf-8"))
        break
    print(data)
    print(f"Sending data to {address}.")