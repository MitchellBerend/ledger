import smtplib
from datetime import datetime
from os import environ
import socket
import lib
from time import time

c = time()

database_login_info = {
    "user":"root",
    "password":environ["db_password"],
    "database":"profile",
    "host":socket.gethostbyname("profile_odin")
}
body = ""
symbols = lib.get_symbols(**database_login_info)
for symbol in symbols:
    total, percentage, current, _100ra = lib.get_total_percentage_current_value_100ra(symbol,**database_login_info)
    body += f"""{str(symbol)}:\n\t100ra:\t\t\t\t{str(_100ra)} vs. {current}\n\tcurrent perf:\t{str(total)}\n\t\t\t\t\t\t\t\t{str(percentage)}%\n\n"""


body += "\n\n\n\t\tThis report was generated automatically by Mitchell Berendhuysen"


with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(environ["email"],environ["password"])

    subject = f"""Portfolio report {str(datetime.now())[:19]}"""
    msg = f"""Subject: {subject}\n\n{body}"""
    print(msg)
    smtp.sendmail(environ["email"], "mitchellbhuysen@hotmail.com",msg)

print(time()-c)