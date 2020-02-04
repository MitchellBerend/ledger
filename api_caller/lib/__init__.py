import os
import requests as r
import mysql.connector as sql
from hashlib import sha224
from datetime import datetime


def retrieve_data(symbol, **login):
    """
    Takes a symbol and login parameters and returns the data.
    """
    con = sql.connect(**login)
    cur = con.cursor()
    cur.execute(
        f"""SELECT DISTINCT * FROM {symbol.replace(".","")};"""
        )
    data = cur.fetchall()
    return data

def format_data(data_dict):
    """
    Takes a list of tuples from the retrieve data function and reformats it into json format.
    """
    data = []
    placeholder = {}
    for index, item  in enumerate(data_dict):
        if index % 8 == 0:
            placeholder["timestamp"] = item[0]
        elif index % 8 == 1:
            placeholder["open"] = item[1]
        elif index % 8 == 2:
            placeholder["high"] = item[2]
        elif index % 8 == 3:
            placeholder["low"] = item[3]
        elif index % 8 == 4:
            placeholder["close"] = item[4]
        elif index % 8 == 5:
            placeholder["volume"] = item[5]
        elif index % 8 == 6:
            placeholder["symbol"] = item[6]
        else:
            data.append(placeholder)
            placeholder = {}
    return data

def get_data_alphavantage(symbol,api_key):
    """
    returns data if call succeeds, returns none otherwise.
    Makes an external api call in the case the data is not already cached.
    """
    headers = {
        "function":"TIME_SERIES_INTRADAY",
        "symbol":f"{symbol}",
        "interval":"15min",
        "apikey":api_key
    }
    url = "https://www.alphavantage.co/query?"
    try:
        print()
        get = r.get(url=url,params=headers,timeout=1.5).text
    except r.exceptions.ConnectTimeout:
        return None
    except r.exceptions.ReadTimeout:
        return None
    if "error" not in get and "Note" not in get:
        get = get.split("\n")[10:-3]
        placeholder = [item.strip()[1:-1] for item in get if "}" not in item]
        #for item in get:
        #    if item.strip() != "},":
        #        placeholder.append(item.strip()[1:-1])
        del get, url, headers
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
            if index % 6 in conversion_dict:
                current_dict[conversion_dict[index % 6][0]] = eval(conversion_dict[index % 6][1])
            else:
                current_dict["volume"] = int(item[13:])
                current_dict["symbol"] = f"{symbol}"
                data.append(current_dict)
                current_dict = {}
        return data
    return None

def add_to_db(data,**login):
    """
    Takes formatted data and login info and adds the data to the database specified in the login info.

    Outputs the result of the queries to stdout.
    """
    con = sql.connect(**login)
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {data[0]["symbol"].replace(".","")} (timestamp varchar(20),open float, high float,low float,close float, volume int, symbol varchar(10), id varchar(56));""")
    con.commit()
    for account in data:
        _hash = sha224(bytes(str(datetime.now()),"utf-8")).hexdigest()
        try:
            cur.execute(f"""INSERT INTO {account["symbol"].replace(".","")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}');""")
            print(f"""query INSERT INTO {account["symbol"].replace(".","")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}'); executed""")
        except:
            print(f"""query INSERT INTO {account["symbol"].replace(".","")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}'); not executed""")
    con.commit()
    con.close()
