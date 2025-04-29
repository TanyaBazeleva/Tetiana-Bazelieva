import sqlite3

def initialize_database():
    conn = sqlite3.connect("transport.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT,
        name TEXT,
        rate_per_ton_km REAL,
        capacity REAL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id INTEGER,
        date TEXT,
        distance REAL,
        FOREIGN KEY(driver_id) REFERENCES drivers(id)
    );
    """)

    conn.commit()
    conn.close()
