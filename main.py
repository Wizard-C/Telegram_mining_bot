import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time

init()
print(Style.BRIGHT + Fore.BLUE)

def console_picture():
    print("  _____          _                           _            ____            _   ")
    time.sleep(0.1)
    print(" |_   _|  _ __  (_)   __ _   _ __     __ _  | |   ___    | __ )    ___   | |_ ")
    time.sleep(0.1)
    print("   | |   | '__| | |  / _` | | '_ \   / _` | | |  / _ \   |  _ \   / _ \  | __|")
    time.sleep(0.1)
    print("   | |   | |    | | | (_| | | | | | | (_| | | | |  __/   | |_) | | (_) | | |_ ")
    time.sleep(0.1)
    print("   |_|   |_|    |_|  \__,_| |_| |_|  \__, | |_|  \___|   |____/   \___/   \__|")
    time.sleep(0.1)
    print("                                     |___/                                    ")
    time.sleep(0.1)
# Просто приколюха
# console_picture()

while (True):
    process = subprocess.Popen([sys.executable, "bot_V2.py"])
    process.wait()
