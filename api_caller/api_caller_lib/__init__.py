import os
import requests as r
import mysql.connector as sql
import yfinance as yf
from hashlib import sha224
from datetime import datetime


def retrieve_data(symbol, **login):
    """
    Takes a symbol and login parameters and returns the data.
    """
    con = sql.connect(**login)

    try:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM cache WHERE symbol_id=(SELECT symbol_id FROM symbol WHERE symbol='{symbol}') ORDER BY timestamp;""")
        data = cur.fetchall()
    finally:
        con.close()
    return data[:100]


def format_data(symbol,data_list):
    data = [
        {   
            "timestamp": date[:10] + " " + date[11:19],
            "close": data_list["Close"][date],
            "volume": data_list["Volume"][date],
            "symbol": symbol
        }
        for date in list(data_list["Open"].keys())
    ]
    data.sort(key=lambda x: x["timestamp"], reverse=True)
    return data[:100]

def get_data_yahoo(symbol):
    ticker = yf.Ticker(symbol)
    data = eval(ticker.history(period="5d",interval="15m").to_json(date_format='iso'))
    del data["Dividends"], data["Stock Splits"]
    return data

def get_data_alphavantage(symbol):
    return format_data(symbol,get_data_yahoo(symbol))

def add_to_db(data, **login):
    """
    Takes formatted data and login info and adds the data to the database specified in the login info.

    Outputs the result of the queries to stdout.
    """
    con = sql.connect(**login)
    try:
        cur = con.cursor()
        cur.execute(
            f"""SELECT symbol_id FROM symbol WHERE symbol='{data[0]['symbol']}';"""
        )
        check = cur.fetchall()
        if not check:
            cur.execute(
                f"""INSERT INTO symbol VALUES ('{data[0]["symbol"]}', (COUNT(SELECT DISTINCT * FROM cache))  ) ;"""
            )
        con.commit()
        for account in data:
            _hash = sha224(bytes(str(datetime.now()), "utf-8")).hexdigest()
            try:
                cur.execute(
                f"""INSERT INTO cache VALUES ('{account["timestamp"]}', {account["close"]}, {account["volume"]}, (SELECT symbol_id FROM symbol WHERE symbol='{account["symbol"]}'), '{_hash}' );"""
                )
                print(f"""INSERT INTO cache VALUES ('{account["timestamp"]}', {account["close"]}, {account["volume"]}, (SELECT symbol_id FROM symbol WHERE symbol='{account["symbol"]}'), '{_hash}' );"""
                )
            except:
                print(f"""INSERT INTO cache VALUES ('{account["timestamp"]}', {account["close"]}, {account["volume"]}, (SELECT symbol_id FROM symbol WHERE symbol='{account["symbol"]}'), '{_hash}' );"""
                )
    finally:
        con.commit()
        con.close()
