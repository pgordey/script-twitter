import time
import sqlite3
import keyboard
import platform
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException




# Функция для обработки учетной записи Twitter
def automate_twitter(email, password, new_password, username):
    # Создание веб-драйвера
    driver = webdriver.Chrome()

    try:
        # Вход в Twitter
        driver.get("https://twitter.com/login")
        time.sleep(4)

        # Вводим email и пароль для входа
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        time.sleep(2)
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Проверка необходимости ввода имени пользователя после почты
        try:
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            if username_input:
                username_input.send_keys(username)
                username_input.send_keys(Keys.ENTER)
                time.sleep(3)
        except TimeoutException:
            print("Имя пользователя после пароля не требуется")

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # Создание поста
        tweet_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class='css-175oi2r r-184en5c']")
            )
        )

        # Клик по полю ввода текста, чтобы сфокусировать его
        tweet_input.click()

        # Пауза для обработки клика
        time.sleep(2)

        keyboard.write("Hello, в это время я родился")
        time.sleep(2)
        

        
        # Цикл будет выполняться один раз и завершится после выполнения нужного действия
        while True:
            # Проверка операционной системы
            if platform.system() == "Darwin":  # macOS
                # Выполнение сочетания клавиш для macOS
                keyboard.press_and_release("command+enter")
            else:  # Предполагается, что это Windows
                # Выполнение сочетания клавиш для Windows
               keyboard.press_and_release("ctrl+enter")
    
            # Завершение цикла
            break
        
        



        # Изменение пароля
        driver.get("https://twitter.com/settings/password")
        time.sleep(3)

        current_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "current_password"))
        )
        new_password_input = driver.find_element(By.NAME, "new_password")
        confirm_new_password_input = driver.find_element(By.NAME, "password_confirmation")

        current_password_input.send_keys(password)
        time.sleep(2)
        new_password_input.send_keys(new_password)
        time.sleep(2)
        confirm_new_password_input.send_keys(new_password)
        time.sleep(2)
        # Подождем, пока кнопка для подтверждения будет кликабельной
        confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[3]/div'))
        )
        # Клик по кнопке подтверждения
        confirm_button.click()

        time.sleep(2)
        
        

        print(f"Обработано {email}")
        
        
        # Сохранение данных в базу данных
        save_to_database(email, password, new_password, username)

    except Exception as e:
        print(f"Ошибка при обработке {email}: {e}")
        
        

    finally:
        # Закрываем веб-драйвер
        driver.quit()
        
        
def save_to_database(email, current_password, new_password, username):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # Создание таблицы для хранения данных учетных записей, если она еще не создана
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS account_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            current_password TEXT NOT NULL,
            new_password TEXT NOT NULL,
            username TEXT
        )
        """
    )

    # Вставка данных учетной записи в таблицу
    cursor.execute(
        """
        INSERT INTO account_info (email, current_password, new_password, username)
        VALUES (?, ?, ?, ?)
        """,
        (email, current_password, new_password, username)
    )

    # Подтверждение изменений и закрытие соединения
    conn.commit()
    conn.close()     


        
        
    
    
    
    # Функция для чтения учетных данных из файла
def read_accounts_from_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        for line in file:
            # Разделяем строку на элементы по точке с запятой
            data = line.strip().split(";")
            if len(data) == 4:
                email, password, new_password, username = data
                accounts.append((email, password, new_password, username))
    return accounts   
        
        
def main():
    # Путь к файлу с учетными данными
    file_path = "account.txt"

    # Читаем учетные данные из файла
    accounts = read_accounts_from_file(file_path)

    # Обрабатываем каждую учетную запись по очереди
    for account in accounts:
        email, password, new_password, username = account
        print(f"Обработка учетной записи: {email}")
        automate_twitter(email, password, new_password, username)        
        
        
        


if __name__ == "__main__":
    main()
