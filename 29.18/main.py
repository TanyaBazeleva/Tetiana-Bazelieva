from wsgiref.simple_server import make_server
import sqlite3
import os
from urllib.parse import parse_qs

DB_PATH = "transport.db"

def render_template(template_name, result=""):
    """Функція для підставлення результату у шаблон HTML"""
    path = os.path.join("templates", template_name)
    with open(path, encoding="utf-8") as file:
        content = file.read()
    return content.replace("$result", str(result))

def application(environ, start_response):
    """Основний WSGI-додаток"""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    if path == '/':
        return ["""
            <h1>Головна сторінка</h1>
            <ul>
                <li><a href="/add_driver">Додати водія</a></li>
                <li><a href="/add_trip">Додати маршрут</a></li>
                <li><a href="/calculate_payment">Розрахувати оплату</a></li>
            </ul>
        """.encode("utf-8")]
    elif path == '/add_driver':
        if method == 'GET':
            return [render_template("add_driver.html").encode()]
        else:  # POST
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = parse_qs(environ['wsgi.input'].read(size).decode())
            surname = data.get('surname', [''])[0]
            name = data.get('name', [''])[0]
            rate = float(data.get('rate', [0])[0])
            capacity = float(data.get('capacity', [0])[0])

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drivers (surname, name, rate_per_ton_km, capacity)
                VALUES (?, ?, ?, ?)
            """, (surname, name, rate, capacity))
            conn.commit()
            conn.close()

            return [render_template("result.html", "Водія успішно додано!").encode()]

    elif path == '/add_trip':
        if method == 'GET':
            return [render_template("add_trip.html").encode()]
        else:  # POST
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = parse_qs(environ['wsgi.input'].read(size).decode())
            driver_id = int(data.get('driver_id', [''])[0])
            date = data.get('date', [''])[0]
            distance = float(data.get('distance', [''])[0])

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trips (driver_id, date, distance)
                VALUES (?, ?, ?)
            """, (driver_id, date, distance))
            conn.commit()
            conn.close()

            return [render_template("result.html", "Маршрут успішно додано!").encode()]

    elif path == '/calculate_payment':
        if method == 'GET':
            return [render_template("calculate_payment.html").encode()]
        else:  # POST
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = parse_qs(environ['wsgi.input'].read(size).decode())
            driver_id = int(data.get('driver_id', [''])[0])
            start_date = data.get('start_date', [''])[0]
            end_date = data.get('end_date', [''])[0]

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Отримати дані про водія
            cursor.execute("""
                SELECT rate_per_ton_km, capacity
                FROM drivers
                WHERE id = ?
            """, (driver_id,))
            driver = cursor.fetchone()

            if driver is None:
                conn.close()
                return [render_template("result.html", "Водія не знайдено!").encode()]

            rate_per_ton_km, capacity = driver

            # Порахувати суму за рейси
            cursor.execute("""
                SELECT SUM(distance)
                FROM trips
                WHERE driver_id = ?
                  AND date BETWEEN ? AND ?
            """, (driver_id, start_date, end_date))
            total_distance = cursor.fetchone()[0]

            conn.close()

            if total_distance is None:
                total_distance = 0

            total_payment = rate_per_ton_km * capacity * total_distance

            return [render_template("result.html", f"Загальна плата за перевезення: {total_payment:.2f} грн").encode()]

    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ["""<h1>404 Сторінку не знайдено</h1>""".encode("utf-8")]

if __name__ == "__main__":
    from db_init import initialize_database
    initialize_database()
    with make_server('', 8080, application) as server:
        print("Сервер працює на http://localhost:8080")
        server.serve_forever()
