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
    "database": "cache",
    "host": socket.gethostbyname("portfolio-db"),
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
    return data


def add_data_to_db(data, **database_login_info):
    for item in data:
        try:
            _hash = hashlib.sha224(bytes(str(datetime.now()), "utf-8")).hexdigest()
            con = sql.connect(**database_login_info)
            cur = con.cursor()
            print(
                f"""INSERT INTO cache.{item["symbol"].replace(".","")} values('{item["timestamp"]}',{round(item["open"],2)}, {round(item["high"],2)}, {round(item["low"],2)}, {round(item["close"],2)}, {item["volume"]}, '{item["symbol"]}', '{_hash}');"""
            )
            cur.execute(
                f"""INSERT INTO cache.{item["symbol"].replace(".","")} values('{item["timestamp"]}' , {item["open"]} , {item["high"]} , {item["low"]}, {item["close"]}, {item["volume"]}, '{item["symbol"]}', '{_hash}' );"""
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
                            Select *, ROW_NUMBER() over(Partition By timestamp order By timestamp) as rownumber
                            from {symbol.replace(".","")}
                            );"""
        )
        cur.execute(f"""DELETE FROM placeholder WHERE rownumber > 1;""")
        cur.execute(f"""ALTER TABLE placeholder drop rownumber;""")
        cur.execute(f"""DROP TABLE {symbol.replace(".","")};""")
        cur.execute(f"""RENAME TABLE placeholder TO {symbol.replace(".","")};""")
        print(f"""deleted dupes from {symbol.replace(".","")}""")
    except:
        print("smtn went wrong")
    finally:
        con.commit()
        con.close()


def get_all_symbols(**database_login_info):
    try:
        con = sql.connect(**database_login_info)
        cur = con.cursor()
        cur.execute("""show tables;""")
        data = [symbol[0] for symbol in cur.fetchall()]
        data1 = []
        for symbol in data:
            cur.execute(f"""SELECT DISTINCT symbol FROM {symbol}""")
            data1.append(cur.fetchone()[0])
        con.close()
        print(data1)
        return data1
    except:
        print("returned none")
        return None


if __name__ == "__main__":
    symbols = get_all_symbols(**database_login_info)
    if symbols != None:
        for symbol in symbols:
            data = call_api(symbol)
            add_data_to_db(data, **database_login_info)
            delete_dupes(symbol, **database_login_info)
            sleep(12)
    else:
        exit()
