import mysql.connector as sql


def show_current(**login_info):
    assert login_info != {}, "Login info not passed as an argument."
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute("""SELECT sum(amount) from wallet;""")
        data = cur.fetchone()[0]
    finally:
        con.commit()
        con.close()
    return data


def deposit_money(amount, **login_info):
    assert login_info != {}, "Login info not passed as an argument."
    amount = float(amount)
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""insert into wallet values ('deposit',{-amount});""")
    finally:
        con.commit()
        con.close()
    return f"""Deposited {amount} into wallet."""


def withdraw_money(amount, **login_info):
    assert login_info != {}, "Login info not passed as an argument."
    amount = float(amount)
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute(f"""insert into wallet values ('withdraw',{-amount});""")
    finally:
        con.commit()
        con.close()
    return f"""Withdrew {amount} from wallet."""
