from telethon import TelegramClient
import sqlite3
import time

db = sqlite3.connect('Account.db')
cur = db.cursor()

# client = TelegramClient('Faas', 1752720, 'a0765766ca82a9b117afbdd139da6e21')
# client.start()

# Создание клиентов через
number_of_iterations = 2
for i in range(1, number_of_iterations+1):
    # Вывод информации о том, какой аккаунт сейчас активируется
    print("Очередь аккаунта № " + str(i))
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{i}'")
    Phone = str(cur.fetchone()[0])
    cur.execute(f"SELECT NAME FROM Account WHERE ID = '{i}'")
    Name = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone + ', ' + Name)
    
    # Вывод его пароля
    cur.execute(f"SELECT PASS FROM Account WHERE ID = '{i}'")
    password = str(cur.fetchone()[0])
    print(password)

    # Копирование из БД его ID и Hash'а
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{i}'")
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{i}'")
    api_hash = str(cur.fetchone()[0])

    # Создание сессии и файла "accoun_'i'"
    session = str("account_" + str(i))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    time.sleep(1)
    if i == iter:
        print("Aккаунты активированы!")
        break
