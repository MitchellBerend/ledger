import smtplib
from datetime import datetime
from os import environ
import socket
import lib


database_login_info = {
    "user":"root",
    "password":environ["db_password"],
    "database":"profile",
    "host":socket.gethostbyname("profile_odin")
}
body = ""
symbols = lib.get_symbols(**database_login_info)
for symbol in symbols:
    total, percentage, current = lib.get_current_performance(symbol,environ["api_caller"],**database_login_info)
    body += f"""{str(symbol)}:\n\t100ra:\t\t\t\t{str(lib.get_api_info(symbol,environ["api_caller"])).rjust(4," ")} vs. {current}\n\tcurrent perf:\t{str(total).rjust(4," ")}\n\t\t\t\t\t\t\t\t{str(percentage*100)}%\n\n"""


body += "\n\n\n\t\tThis report was generated automatically by Mitchell Berendhuysen"


with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(environ["email"],environ["password"])

    subject = f"""Portfolio report {str(datetime.now())[:19]}"""
    msg = f"""Subject: {subject}\n\n{body}"""
    print(msg)
    smtp.sendmail(environ["email"], "mitchellbhuysen@hotmail.com",msg)