import smtplib
from datetime import datetime
from os import environ
import socket
import lib
from time import time


database_login_info = {
    "user": environ["db_user"],
    "password": environ["db_password"],
    "database": "profile",
    "host": socket.gethostbyname("profile_odin"),
}

lib.insert_total_diff(**database_login_info)

total_res = 0
body = ""
symbols = lib.get_symbols(**database_login_info)
for symbol in symbols:
    (
        total,
        percentage,
        current,
        _100ra,
        price_of_purchase,
    ) = lib.get_total_percentage_current_value_100ra(symbol, **database_login_info)
    body += f"""{str(symbol)}:\n\t100ra:\t\t\t\t{str(_100ra)}\n\tCurrent\t\t\t{current}\n\tBought for:\t\t{price_of_purchase}\n\tCurrent perf:\t\t{str(total)}\n\t\t\t\t\t\t\t\t{str(percentage)}%\n\n"""
    total_res += total

body += f"""\nTotal combined: {round(total_res,2)}\n\n\t\tThis report was generated automatically by Mitchell Berendhuysen"""


with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(environ["email"], environ["password"])

    subject = f"""Portfolio report {str(datetime.now())[:19]}"""
    msg = f"""Subject: {subject}\n\n{body}"""
    print(msg)
    smtp.sendmail(environ["email"], environ["target_email"], msg)

