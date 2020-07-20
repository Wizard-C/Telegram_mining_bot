from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import requests
import json
import hashlib
import time
import re
from telethon import TelegramClient
import webbrowser
import urllib.request
import os
import sqlite3

class RunChromeTests():
    def testMethod(self):
        selenium_url = "http://localhost:4444/wd/hub"
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 10)
        driver.close()
        driver.quit()

db = sqlite3.connect('Account.db')
cur = db.cursor()

number_of_iterations = 2
start = 1

for i in range(start, number_of_iterations+1):
    complete_task = 0
    no_task = 0
    # Вывод имени аккаунта в очереди
    print("Очередь аккаунта № " + str(i))
    cur.execute(f"SELECT NAME FROM Account WHERE ID = '{i}'")
    Name = str(cur.fetchone()[0])
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{i}'")
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт. Имя: " + Name + '\nТелефон: ' + Phone)

    # Копирование из БД ID и Hash'a
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{i}'")
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{i}'")
    api_hash = str(cur.fetchone()[0])
    # Создание сессии
    session = str("account_" + str(i))
    client = TelegramClient(session, api_id, api_hash)
    client.start()

    # Нахождение нужного диалога
    dialogues = client.get_dialogs()
    for dialog in dialogues:
        if dialog.title == 'LTC Click Bot':
            dialog_LTC = dialog
            break

    client.send_message('LTC Click Bot', "🖥 Visit sites")
    time.sleep(3)
    # Цикл выполнения заданий
    while True:
        time.sleep(2)
        # Если дважды нет заданий, меняется аккаунт
        print("Нет заданий уже: " + str(no_task) + " раз")
        if no_task == 2:
            print("Переходим на другой аккаунт, причина: 'Нет заданий'")
            break
        # Если выполненно 10 заданий, меняется аккаунт
        print("Выполненно заданий: " + str(complete_task))
        if complete_task == 10:
            print("Переходим на другой аккаунт, причина: 'Выполнено 10 заданий'")
            break
        
        dialogues = client.get_messages(dialog_LTC, limit=1)
        for dialog in dialogues:
            # Ставим исключение. Возникает принудительный разрыв сервера
            try:
                # Если есть фраза "to get your reward", тогда выполняем просмотр рекламы
                if re.search('to get your reward', dialog.message):
                    print("Найдено задание")
                    print('\n', dialog.message)
                    dialog = str(dialog.message)
                    dialog = dialog.replace('You must stay on the site for', '').replace('seconds to get your reward.', '')
                    waitin = int(dialog)
                    print ("Ждать придется: ", waitin)
                    client.send_message('LTC Click Bot', "/visit")
                    time.sleep(1)
                    dialogues_new = client.get_messages(dialog_LTC, limit=1)
                    for dialog_new in dialogues_new:
                        button_data = dialog_new.reply_markup.rows[1].buttons[1].data
                        message_id = dialog_new.id
                        print("Перехожу по ссылке")
                        time.sleep(2)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        ch = RunChromeTests()
                        ch.testMethod()
                        fp = urllib.request.urlopen(url_rec)
                        mybytes = fp.read()
                        mystr = mybytes.decode("utf8")
                        fp.close()
                        if re.search('Switch to reCAPTCHA', mystr):
                            resp = client(GetBotCallbackAnswerRequest(
                                'LTC Click Bot',    
                                message_id,
                                data=button_data
                            ))
                            print("КАПЧА!")

                        else:
                            time.sleep(2)
                elif re.search('Sorry', dialog.message):
                    print("Найдено Sorry")
                    no_task = no_task + 1
                    print(no_task)

                else:
                    messages = client.get_messages('Litecoin_click_bot')
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    f = open("per10.txt")
                    fd = f.read()
                    if fd == url_rec: 
                        print("Найдено повторение переменной")
                        dialogues_new = client.get_messages(dialog_LTC, limit=1)
                        for dialog_new in dialogues_new:
                            button_data = dialog_new.reply_markup.rows[1].buttons[1].data
                            message_id = dialog_new.id
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = client(GetBotCallbackAnswerRequest(
                                dialog_LTC,
                                message_id,
                                data=button_data
                            ))
                            time.sleep(2)
                    else:
                        waitin = 15
                        data1 = requests.get(url_rec).json
                        print(data1)

                        my_file = open('per10.txt', 'w')
                        my_file.write(url_rec)
                        print("Новая запись в файле сделана")
                        time.sleep(4)
                        complete_task = complete_task + 1

                print('\nЦикл')
            except BaseException as err:
                print('ERROR')
                print(err)
    time.sleep(1)
