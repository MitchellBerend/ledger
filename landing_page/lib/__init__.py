import mysql.connector as sql


def get_name_price_amount(**login_info):
    assert login_info != {}, "Check login_info variable!"
    con = sql.connect(**login_info)
    try:
        cur = con.cursor()
        cur.execute("""SELECT name,price_of_purchase,amount,date_of_purchase FROM profile;""")
        tup = cur.fetchall()
    finally:
        con.close()
    data = [{str(item[0]):{"price of purchase":item[1],"amount":item[2],"total":item[1]*item[2],"date of purchase":item[3]}} for item in tup]
    return data