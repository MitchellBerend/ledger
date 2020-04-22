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
        cur.execute(f"""SELECT * FROM {symbol.replace(".", "")} order by timestamp;""")
        data = cur.fetchall()
    finally:
        con.close()
    return data[:100]


def format_data(symbol,data_list):
    data = []
    dates = list(data_list["Open"].keys())
    for date in dates:
        data.append(
            {
            "timestamp": date[:10] + " " + date[11:19],
            "open": data_list["Open"][date],
            "high": data_list["High"][date],
            "low": data_list["Low"][date],
            "close": data_list["Close"][date],
            "volume": data_list["Volume"][date],
            "symbol": symbol
            }
        )
    data.sort(key=lambda x: x["timestamp"], reverse=True)
    return data[:100]


def get_data_yahoo(symbol):
    ticker = yf.Ticker(symbol)
    data = eval(ticker.history(period="5d",interval="15m").to_json(date_format='iso'))
    del data["Dividends"], data["Stock Splits"]
    return data

def get_data_alphavantage(symbol, api_key):
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
            f"""CREATE TABLE IF NOT EXISTS {data[0]["symbol"].replace(".", "")} (timestamp varchar(20),open float, high float,low float,close float, volume int, symbol varchar(10), id varchar(56));"""
        )
        con.commit()
        for account in data:
            _hash = sha224(bytes(str(datetime.now()), "utf-8")).hexdigest()
            try:
                cur.execute(
                    f"""INSERT INTO {account["symbol"].replace(".", "")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}');"""
                )
                print(
                    f"""query INSERT INTO {account["symbol"].replace(".", "")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}'); executed"""
                )
            except:
                print(
                    f"""query INSERT INTO {account["symbol"].replace(".", "")} values('{account["timestamp"]}', {account["open"]}, {account["high"]}, {account["low"]}, {account["close"]}, {account["volume"]}, '{account["symbol"]}', '{_hash}'); not executed"""
                )
    finally:
        con.commit()
        con.close()
