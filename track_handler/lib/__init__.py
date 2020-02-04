import mysql.connector as sql
import os
import requests as r
from datetime import datetime
import socket
"""

CREATE TABLE profile (
    name varchar(10),
    price_of_purchase float,
    date_of_purchase varchar(10),
    amount int,
    total_value float
);


test to make sure it works with a period
"""



def request_checker(data):
    return data[-1]


def make_api_request(symbol):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname("api_caller"),5000))
    sock.send(bytes(str(symbol), "utf-8"))
    data = ""
    while True:
        msg = sock.recv(1024)
        if len(msg) <= 0:
            break
        data += msg.decode("utf-8")
    data = eval(data)
    return data[0]["close"]

def insert_data_in_profile(symbol,price_of_purchase,amount,**login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO profile VALUES (
        '{symbol.upper()}',
        {price_of_purchase},
        '{str(datetime.now())[:-16]}',
        {amount},
        {price_of_purchase * int(amount)});""")
    except:
        print("catch")
    finally:
        con.commit()
        con.close()


def check_profile_for_existing_data(symbol,**login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM profile WHERE name='{symbol.upper()}';""")
        print(f"""SELECT * FROM profile WHERE name='{symbol.upper()}';""")
        count = cur.fetchall()
    finally:
        con.close()
    
    if len(count) > 0:
        return True
    return False

def delete_data_from_profile(symbol,**login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""DELETE FROM profile WHERE name='{symbol}';""")
        print("pass")
    except:
        print("catch")
    finally:
        con.commit()
        con.close()
