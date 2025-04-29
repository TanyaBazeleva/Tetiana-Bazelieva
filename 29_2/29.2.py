from wsgiref.simple_server import make_server
from string import Template
import cgi
import sqlite3
import openpyxl
import os

OPTION = """
    <option value="$cur_id">$cur_name</option>
"""
class ExchangeRateDB:

    def __init__(self, database):
        self.database = database

    def get_currencies(self):
        """ Повертає список валют з БД """
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        curs.execute("""SELECT * FROM currencies""")
        currencies = curs.fetchall()
        conn.close()
        return currencies

    def obtain_rate(self, cur1_id, cur2_id, amount):
        """ Повертає курс валюти cur1_id відносно валюти cur2_id """
        if cur1_id == cur2_id:
            return amount
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        query = """
        SELECT "rate" FROM "exchange_rates"
        WHERE "cur1_id"=? AND "cur2_id"=?
        """
        result = 0
        curs.execute(query, (cur1_id, cur2_id))
        rate = curs.fetchone()
        if rate is not None:
            result = amount * rate[0]
        curs.execute(query, (cur2_id, cur1_id))
        rate = curs.fetchone()
        if rate is not None:
            result = amount / rate[0]
        conn.close()
        return result

    def get_currency_name(self, currency_id):
        """ Повертає ім’я валюти згідно її id """
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        curs.execute(
            """SELECT "name" FROM "currencies" WHERE "id"=?""",
            (currency_id,)
        )
        name = curs.fetchone()
        conn.close()
        return name[0]

    def currency_exists(self, currency_id, currency_name):
        """ Перевіряє чи існує валюта з заданим кодом або назвою """
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        result = True
        curs.execute(
            """SELECT * FROM "currencies" WHERE "id"=? OR "name"=?""",
            (currency_id, currency_name)
        )
        if curs.fetchone() is None:
            result = False
        conn.close()
        return result

    def add_currency(self, new_cur_id, new_cur_name, reg_cur_id, rate):
        """Додає нову валюту до БД.

        :param new_cur_id: код нової валюти
        :param new_cur_name: назва нової валюти
        :param reg_cur_id: код валюти, відносно якої надається курс
        :param rate: курс валюти
        :return:
        """
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        curs.execute("""SELECT "id" FROM "currencies";""")
        currencies_id = curs.fetchall()  # Поточні валюти в БД

        # Додаємо валюту в БД
        curs.execute(
            """INSERT INTO "currencies" VALUES (?, ?);""",
            (new_cur_id, new_cur_name)
        )

        # Якщо окрім нової валюти є ще валюти, встановлюємо курс
        if len(currencies_id) > 0:
            query = """INSERT INTO "exchange_rates" VALUES (?, ?, ?);"""
            curs.execute(query, (new_cur_id, reg_cur_id, rate))
            currencies_id.remove((reg_cur_id,))

            for cur_id in currencies_id:
                reg_rate = self.obtain_rate(reg_cur_id, cur_id[0], rate)
                curs.execute(query, (new_cur_id, cur_id[0], reg_rate))

        conn.commit()
        conn.close()

    def update_currency_name(self, cur_id, new_cur_name):
        """Надає нове ім’я new_cur_name валюті з кодом cur_id"""
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        curs.execute(
            """UPDATE "currencies" SET "name"=? WHERE "id"=?;""",
            (new_cur_name, cur_id)
        )
        conn.commit()
        conn.close()

    def update_currency_rate(self, upd_cur_id, reg_cur_id, upd_rate):
        """Змінює курс валюти upd_cur_id відносно валюти reg_cur_id
        і, відповідно, змінює курси інших валют відносно upd_cur_id.
        """
        conn = sqlite3.connect(self.database)
        curs = conn.cursor()
        curs.execute(
            """SELECT "id" FROM "currencies" WHERE "id"<>?;""",
            (upd_cur_id,)
        )
        currencies_id = curs.fetchall()  # Всі валюти окрім поточної
        # Якщо є інші валюти в БД і є валюти, оновлюємо курс
        if len(currencies_id) > 0:
            query = """
            UPDATE "exchange_rates" SET "rate"=?
            WHERE "cur1_id"=? AND "cur2_id"=?;
            """
            # Виконуємо не один, а два наступних запити
            curs.execute(query, (upd_rate, upd_cur_id, reg_cur_id))
            curs.execute(query, (1 / upd_rate, reg_cur_id, upd_cur_id))
            for cur_id in currencies_id:
                reg_rate = self.obtain_rate(reg_cur_id, cur_id[0], upd_rate)
                curs.execute(query, (reg_rate, upd_cur_id, cur_id[0]))
                curs.execute(query, (1/reg_rate, cur_id[0], upd_cur_id))
        conn.commit()
        conn.close()

        def delete_currency(self, currency_id):
            """Видаляє з БД валюту з кодом currency_id"""
            conn = sqlite3.connect(self.database)
            curs = conn.cursor()
            curs.execute(
                """DELETE FROM "currencies" WHERE "id"=?;""",
                (currency_id,)
            )
            curs.execute(
                """DELETE FROM "exchange_rates"
                WHERE "cur1_id"=? OR "cur2_id"=?;""",
                (currency_id, currency_id)
            )
            conn.commit()
            conn.close()

        def __call__(self, environ, start_response):
            path = environ.get("")







