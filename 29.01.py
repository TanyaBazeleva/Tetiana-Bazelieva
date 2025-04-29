import sqlite3
import openpyxl
import os

def from_excel(xlsx_filename) -> dict:
    """
    Зчитує дані з Excel-файлу та повертає словник з ключами - ім’я аркуша
    та значеннями - список рядків (список клітинок) аркуша.

    :param xlsx_filename: назва Excel-файлу
    :return: словник робочих аркушів Excel
    """
    wb = openpyxl.load_workbook(xlsx_filename)
    sheets = {}
    for ws in wb:
        sheets[ws.title] = [
            [cell.value for cell in row]
            for row in ws.rows
        ]
    return sheets
def to_database(db_filename, sheets):
    """
    Зберігає дані підприємства з робочих аркушів у БД.

    :param db_filename: назва БД
    :param sheets: словник робочих аркушів Excel-файлу
    :return:
    """
    if os.path.exists(db_filename):
        os.remove(db_filename)

    # Створюємо зв'язок з базою даних
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    # Створюємо таблицю departments
    curs.execute(
        """
        CREATE TABLE departments (
            id INTEGER NOT NULL,
            title TEXT UNIQUE,
            PRIMARY KEY (id AUTOINCREMENT)
        );
        """
    )

    for row in sheets["departments"][1:]:
        # Додати рядок row в таблицю departments
        curs.execute(
            """
            INSERT INTO departments
            VALUES (?, ?);
            """,
            row
        )

    # Створюємо таблицю staff
    # Створюємо таблицю staff
    curs.execute(
        """
        CREATE TABLE staff (
            id INTEGER NOT NULL,
            personnel_number TEXT UNIQUE,
            last_name TEXT,
            first_name TEXT,
            second_name TEXT,
            passport TEXT,
            salary REAL,
            department_id INTEGER,
            PRIMARY KEY (id AUTOINCREMENT),
            FOREIGN KEY (department_id)
                REFERENCES departments (department_id)
        );
        """
    )
    # Створюємо таблицю staff
    curs.execute(
        """
        CREATE TABLE staff (
            id INTEGER NOT NULL,
            personnel_number TEXT UNIQUE,
            last_name TEXT,
            first_name TEXT,
            second_name TEXT,
            passport TEXT,
            salary REAL,
            department_id INTEGER,
            PRIMARY KEY (id AUTOINCREMENT),
            FOREIGN KEY (department_id)
                REFERENCES departments (department_id)
        );
        """
    )
    # Додати рядки в таблицю staff
    curs.executemany(
        """
        INSERT INTO staff (
            personnel_number,
            last_name,
            first_name,
            second_name,
            passport,
            salary,
            department_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        sheets["staff"][1:]
    )

    conn.commit()  # Фіксуємо транзакцію
    conn.close()  # Закриваємо зв’язок з БД

def print_data(db_filename):
    """
    Виводить всі дані з БД підприємства

    :param db_filename: назва БД
    :return:
    """
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    curs.execute(
        """
        SELECT * FROM staff;
        """
    )
    table = curs.fetchall()
    print("staff:")
    for row in table:
        print(*row)

    curs.execute(
        """
        SELECT * FROM "departments";
        """
    )
    table = curs.fetchall()
    print("departments:")
    for row in table:
        print(*row)

    conn.close()
def delete_department(db_filename, department_title):
    """
    Видалення підрозділу з БД разом з усіма робітниками,
    що працюють у цьому підрозділі.

    :param db_filename: назва БД
    :param department_title: назва підрозділу
    :return:
    """
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    # Знаходимо id підрозділу
    curs.execute(
        """
        SELECT id FROM departments
        WHERE title=?;
        """,
        (department_title,)
    )
    dep_id = curs.fetchone()
    if dep_id:
        curs.execute(
            """
            DELETE FROM "departments"
            WHERE id=?;
            """,
            dep_id
        )
        curs.execute(
            """
            DELETE FROM "staff"
            WHERE department_id=?;
            """,
            dep_id
        )

    conn.commit()
    conn.close()
def id_salary_range(db_filename, low_fork, high_fork):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    # Знаходимо id підрозділу
    curs.execute(
        """
        SELECT personnel_number FROM staff
        WHERE salary>20000.00 AND salary<30000.00;
        """,
        (low_fork, high_fork,)
    )
    personal_ids = curs.fetchall()
    print("workers:")
    for row in personal_ids:
        print(*row)
    conn.close()
def archive_workers(db_filename):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """
        SELECT last_name, first_name, second_name FROM staff
        WHERE department_id = (
            SELECT department_id FROM departments
            WHERE title = 'Архів'
        );
        """, (bd_filename)
    )
    staff = curs.fetchall()
    print("workers archive:")
    for row in staff:
        print(*row)
    conn.close()
def production_workers(db_filename):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()

    curs.execute(
        """
        SELECT COUNT(*) FROM staff
        WHERE department_id IN (
            SELECT department_id FROM departments
            WHERE title='Бухгалтерія' OR title='Виробництво'
        );
        """, (db_filename)
    )
    production = curs.fetchall()
    print("workers production: ", production[0])
    conn.close()



if __name__ == "__main__":
    xlsx = "enterprises.xlsx"
    db = "enterprise.db"
    worksheets = from_excel(xlsx)
    to_database(db, worksheets)
    print_data(db)
    delete_department(db, "Бухгалтерія")
    print_data(db)
"""
SELECT personnel_number FROM staff
WHERE salary>20000.00 AND salary<30000.00;
"""
# Отримати ПІБ всіх працівників, які працюють у Архіві
"""
SELECT last_name, first_name, second_name FROM staff
WHERE department_id = (
    SELECT department_id FROM departments
    WHERE title = 'Архів'
);
"""











