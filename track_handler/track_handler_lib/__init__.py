import mysql.connector as sql
import os
import requests as r
from datetime import datetime
import socket


def request_checker(data):
    return data[-1]


def make_api_request(symbol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname("api_caller"), 5000))
    sock.send(bytes(str(symbol), "utf-8"))
    data = ""
    while True:
        msg = sock.recv(1024)
        if len(msg) <= 0:
            break
        data += msg.decode("utf-8")
    data = eval(data)
    return data[0]["close"]


def insert_data_in_profile(symbol, price_of_purchase, amount, **login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO profile VALUES ( '{str(datetime.now())[:-16]}', {price_of_purchase}, {amount}, (SELECT symbol_id FROM symbol WHERE symbol='{symbol.upper()}' );"""
        )
    finally:
        con.commit()
        con.close()


def check_profile_for_existing_data(symbol, **login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM profile WHERE symbol_id=(SELECT symbol_id FROM symbol WHERE symbol='{symbol.upper()}');""")
        count = cur.fetchall()
    finally:
        con.close()
    if len(count) > 0:
        return True
    return False


def delete_data_from_profile(symbol, **login_info):
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""DELETE FROM profile WHERE symbol_id=(SELECT symbol_id FROM symbol WHERE symbol='{symbol}');""")
    finally:
        con.commit()
        con.close()


def get_value_from_api(symbol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname("api_caller"), 5000))
    sock.send(bytes(str(symbol), "utf-8"))
    data = ""
    while True:
        msg = sock.recv(1024)
        if len(msg) <= 0:
            break
        data += msg.decode("utf-8")
    data = eval(data)
    return float(data[0]["close"])


def add_wallet(symbol, **login_info):
    assert login_info != {}, "Login info not passed as an argument."
    value = get_value_from_api(symbol)
    assert value != 0, "Amount was not retrieved."
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""select amount from profile where symbol_id=(select symbol_id from symbol where symbol='{symbol}');""")
        amount = float(cur.fetchone()[0])
        fee = value * amount * 0.0005
        if fee < 1.25:
            fee = 1.25
        elif fee > 29:
            fee = 29
        cur.execute(f"""INSERT INTO wallet values ( (SELECT symbol_id FROM symbol WHERE symbol='{symbol}'), {amount*value});""")
        cur.execute(f"""INSERT INTO wallet values ( (SELECT symbol_id FROM symbol WHERE symbol='{symbol}'), {-fee});""")
    finally:
        con.commit()
        con.close()


def subtract_wallet(symbol, amount, **login_info):
    assert login_info != {}, "Login info not passed as an argument."
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute("""SELECT sum(amount) FROM wallet;""")
        wallet = cur.fetchone()[0]
        print(wallet)
        fee = amount * 0.0005
        if fee < 1.25:
            fee = 1.25
        elif fee > 29:
            fee = 29
        cur.execute(f"""INSERT INTO wallet values ( (SELECT symbol_id FROM symbol WHERE symbol='{symbol}'), {-amount});""")
        cur.execute(f"""INSERT INTO wallet values ( (SELECT symbol_id FROM symbol WHERE symbol='{symbol}'), {-fee});""")
    finally:
        con.commit()
        con.close()
