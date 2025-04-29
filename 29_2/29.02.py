import requests
import sqlite3
from datetime import datetime

DB_PATH = "text.db"
API_URL = " https://v6.exchangerate-api.com/v6/YOUR-API-KEY"
key = '84684hdh2o29930'
# Створення бази даних і таблиць
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency1 TEXT,
            currency2 TEXT,
            rate REAL,
            updated_at TEXT,
            PRIMARY KEY (currency1, currency2),
            FOREIGN KEY (currency1) REFERENCES currencies(code),
            FOREIGN KEY (currency2) REFERENCES currencies(code)
        );
    """)
    # Додавання базових валют
    cursor.execute("""
        INSERT OR IGNORE INTO currencies (code, name) VALUES
        ('UAH', 'Українська гривня'),
        ('USD', 'Долар США'),
        ('EUR', 'Євро')
    """)
    conn.commit()
    cursor.close()
    conn.close()
# Отримання списку валют з бази даних
def get_currency_codes(cursor):
    cursor.execute("SELECT code FROM currencies;")
    return [row[0] for row in cursor.fetchall()]
def update_exchange_rates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    currencies = get_currency_codes(cursor)

    for base_currency in currencies:
        print(base_currency)
        try:
            response = requests.get(API_URL + base_currency)
            print(API_URL + base_currency)
            # GET https://v6.exchangerate-api.com/v6/YOUR-API-KEY
            data = response.json()
            print(data)
            rates = data.get("conversion_rates", {})
            print('rates:', rates)

            for target_currency, rate in rates.items():
                print(target_currency, rate)
                if target_currency in currencies:
                    cursor.execute("""
                        INSERT INTO exchange_rates (currency1, currency2, rate, updated_at)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(currency1, currency2) DO UPDATE SET rate = excluded.rate, updated_at = excluded.updated_at;
                    """, (base_currency, target_currency, rate, datetime.now()))
        except Exception as e:
            print("Error:", e)

    conn.commit()
    cursor.close()
    conn.close()
def display_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    cursor.close()
    conn.close()
# Відображення всіх записів у таблицях
def display_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\nCurrencies Table:")
    cursor.execute("SELECT * FROM currencies;")
    for row in cursor.fetchall():
        print(row)

    print("\nExchange Rates Table:")
    cursor.execute("SELECT * FROM exchange_rates;")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()
if __name__ == "__main__":
    initialize_database()
    display_tables()
    display_records()
    update_exchange_rates()
    print('Exchange rates updated successfully!')
    # pr_tbl('currencies')
    # display_tables()
    display_records()


