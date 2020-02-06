import mysql.connector as sql
from os import environ
import requests as r
import hashlib
from datetime import datetime
from socket import gethostbyname
from time import sleep

database_login_info = {
    "user":environ["db_user"],
    "password":environ["db_password"],
    "database":"cache",
    "host":gethostbyname("portfolio-db")
}


def call_alpha_api(symbol):
    headers = {
        "function":"TIME_SERIES_INTRADAY",
        "symbol":f"{symbol}",
        "interval":"15min",
        "apikey":environ["api_caller"]
    }
    url = "https://www.alphavantage.co/query?"
    get = r.get(url=url,params=headers)
    del url, headers
    get = get.text
    get = get.split("\n")[10:-3]
    placeholder = [item.strip()[1:-1] for item in get if item.strip() != "},"]
    del get
    data = []
    current_dict = {}
    for index, item in enumerate(placeholder):
        conversion_dict ={
            0:["timestamp","item[:-3]"],
            1:["open", "float(item[11:-1])"],
            2:["high","float(item[11:-1])"],
            3:["low", "float(item[10:-1])"],
            4:["close","float(item[12:-1])"]
        }
        if (index % 6) in conversion_dict:
            current_dict[conversion_dict[index % 6][0]] = eval(conversion_dict[index % 6][1])
        else:
            current_dict["volume"] = int(item[13:])
            current_dict["symbol"] = f"{symbol}"
            data.append(current_dict)
            current_dict = {}
    return data


def add_data_to_db(data, **database_login_info):
    for item in data:
        try:
            _hash = hashlib.sha224(bytes(str(datetime.now()),"utf-8")).hexdigest()
            con = sql.connect(**database_login_info)
            cur = con.cursor()
            print(f"""INSERT INTO cache.{item["symbol"].replace(".","")} values('{item["timestamp"]}',\t{item["open"]},\t{item["high"]},\t{item["low"]},\t{item["close"]},\t{item["volume"]},\t'{item["symbol"]}',\t'{_hash}');""")
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
        cur.execute(f"""create table placeholder as
                            (
                            Select *, ROW_NUMBER() over(Partition By timestamp order By timestamp) as rownumber
                            from {symbol.replace(".","")}
                            );""")
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
        print('returned none')
        return None


if __name__ == "__main__":
    symbols = get_all_symbols(**database_login_info)
    if symbols != None:
        for symbol in symbols:
            data = call_alpha_api(symbol)
            add_data_to_db(data,**database_login_info)
            delete_dupes(symbol,**database_login_info)
            sleep(12)
    else:
        exit()
