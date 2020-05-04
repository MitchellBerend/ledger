import mysql.connector as sql
import requests as r
import hashlib
import socket
from datetime import datetime
from time import sleep
from os import environ

database_login_info = {
    "user": environ["db_user"],
    "password": environ["db_password"],
    "database": "odin",
    "host": socket.gethostbyname("portfolio_db"),
}


def call_api(symbol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname("api_caller"), 5000))
    sock.send(bytes(symbol, "utf-8"))
    data = ""
    while True:
        msg = sock.recv(1024)
        if len(msg) <= 0:
            break
        data += msg.decode("utf-8")
    sleep(.5)
    return eval(data)


def add_data_to_db(data, **database_login_info):
    for item in data:
        try:
            _hash = hashlib.sha224(bytes(str(datetime.now()), "utf-8")).hexdigest()
            con = sql.connect(**database_login_info)
            cur = con.cursor()
            print(
                f"""INSERT INTO cache VALUES ('{item["timestamp"]}', {round(item["close"],2)}, {item["volume"]}, (SELECT symbol_id FROM symbol WHERE symbol='{item["symbol"]}'), '{_hash}' );"""
            )
            cur.execute(
                f"""INSERT INTO cache VALUES ('{item["timestamp"]}', {item["close"]}, {item["volume"]}, (SELECT symbol_id FROM symbol WHERE symbol='{item["symbol"]}'), '{_hash}' );"""
            )
        finally:
            con.commit()
            con.close()


def delete_dupes(symbol, **database_login_info):
    try:
        con = sql.connect(**database_login_info)
        cur = con.cursor()
        cur.execute(
            f"""create table placeholder as
                            (
                            Select *, ROW_NUMBER() over(Partition By timestamp, symbol_id order By timestamp) as rownumber
                            from cache
                            );"""
        )
        cur.execute(f"""DELETE FROM placeholder WHERE rownumber > 1;""")
        cur.execute(f"""ALTER TABLE placeholder drop rownumber;""")
        cur.execute(f"""DROP TABLE cache;""")
        cur.execute(f"""RENAME TABLE placeholder TO cache;""")
        print(f"""deleted dupes from cache""")
    except:
        print("smtn went wrong")
    finally:
        con.commit()
        con.close()


def get_all_symbols(**database_login_info):
    try:
        con = sql.connect(**database_login_info)
        cur = con.cursor()
        cur.execute("""SELECT symbol FROM symbol where symbol_id>=0;""")
        data = [symbol[0] for symbol in cur.fetchall()]
        return data
    except:
        print("returned none")
        return None
    finally:
        con.close()


if __name__ == "__main__":
    symbols = get_all_symbols(**database_login_info)
    if symbols != None:
        for symbol in symbols:
            data = call_api(symbol)
            add_data_to_db(data, **database_login_info)
            delete_dupes(symbol, **database_login_info)
            sleep(2)
    else:
        exit()
