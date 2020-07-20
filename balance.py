import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json


db = sqlite3.connect('Account.db')
cur = db.cursor()

number_of_iterations = 2
total_amount = 0
try:
    for i in range(1, number_of_iterations+1):
        cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{i}'")
        Phone = str(cur.fetchone()[0])
        print("Аккаунт: " + Phone, end=', ')
        cur.execute(f"SELECT NAME FROM Account WHERE ID = '{i}'")
        Name = str(cur.fetchone()[0])
        print(Name)

        cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{i}'")
        api_id = str(cur.fetchone()[0])
        cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{i}'")
        api_hash = str(cur.fetchone()[0])
        session = str("anon" + str(i))
        client = TelegramClient(session, api_id, api_hash)
        client.start()

        dialogues = client.get_dialogs()
        for dialog in dialogues:
            if dialog.title == 'LTC Click Bot':
                dialog_LTC = dialog
                break

        client.send_message('LTC Click Bot', "/balance")
        time.sleep(1)
        messages = client.get_messages(dialog_LTC, limit=1)

        for msg in messages:
            message_text = str(msg.message)
            balance_text = message_text.replace('Available balance: ', '')
            balance_text = balance_text.replace(' LTC', '')
            print(balance_text, ' LTC')
            print('{:.2f}'.format(float(balance_text)*3107), ' RUB')
            amount_now = float(balance_text)

        total_amount = '{: .8f}'.format(total_amount + amount_now)
        time.sleep(1)
        if i == number_of_iterations:
            print("\nВсего добыто LTC: ", str(total_amount))
            print("Всего добыто RUB: ", '{: .2f}'.format(float(total_amount)*3107))
            break
except:
    print("\nВсего добыто LTC: ", str(total_amount))
    print("Всего добыто RUB: ", '{: .2f}'.format(float(total_amount)*3107))
    print('Ошибка, преждевременный выход из цикла')