import sqlite3

db = sqlite3.connect('Account.db')
cur = db.cursor()
    # Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    NAME TEXT,
    PHONE TEXT,
    PASS TEXT,
    API_ID TEXT,
    API_HASH TEXT,
    ACTIVITY TEXT,
    LITECOIN TEXT
)""")

db.commit()

Name = input('Введи Name: ')
Phone = input('Введи Phone: ')
Password = input('Введи Password: ')
Api_id = input('Введи Api_id: ')
Api_hash = input('Введи Api_hash: ')

# example
# Name = "Vi"
# Phone = "+79640129434"
# Password = "pgpfdgpdfgr"
# Api_id = "1645818"
# Api_hash = "77ebd7eea17f32b3ce68df83c493899c"
Activity = "ON"
Litecoin = "ltc1qwpmykrnd7s56w3jtlcd5gxuxak9q0dpna8w498"

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(NAME, PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN) VALUES (?,?,?,?,?,?,?);""",
                (Name, Phone, Password, Api_id, Api_hash, Activity, Litecoin))
    db.commit()
    print("Зарегистрированно!")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)
