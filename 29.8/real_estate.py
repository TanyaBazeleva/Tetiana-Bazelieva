import sqlite3

def connect_db():
    return sqlite3.connect("real_estate.db")

def add_object(obj_type, address, total_area, rooms_count):
    with connect_db() as conn:
        conn.execute('''
            INSERT INTO objects (type, address, total_area, rooms_count)
            VALUES (?, ?, ?, ?)
        ''', (obj_type, address, total_area, rooms_count))
        conn.commit()

def add_room(object_id, purpose, area):
    with connect_db() as conn:
        conn.execute('''
            INSERT INTO rooms (object_id, purpose, area)
            VALUES (?, ?, ?)
        ''', (object_id, purpose, area))
        conn.commit()

def filter_objects_by_type_and_area(obj_type, min_area):
    with connect_db() as conn:
        cursor = conn.execute('''
            SELECT * FROM objects WHERE type = ? AND total_area >= ?
        ''', (obj_type, min_area))
        return cursor.fetchall()

def show_full_info():
    with connect_db() as conn:
        cursor = conn.execute('''
            SELECT o.id, o.type, o.address, o.total_area, o.rooms_count,
                   r.purpose, r.area
            FROM objects o
            LEFT JOIN rooms r ON o.id = r.object_id
            ORDER BY o.id
        ''')
        return cursor.fetchall()

# Додаткове меню для прикладу використання
if __name__ == "__main__":
    print("\n--- БАЗА НЕРУХОМОСТІ ---")
    print("1. Додати об'єкт")
    print("2. Додати кімнату")
    print("3. Показати повну інформацію")
    print("4. Пошук за видом і площею")
    choice = input("Оберіть дію: ")

    if choice == '1':
        t = input("Тип об'єкта: ")
        a = input("Адреса: ")
        s = float(input("Загальна площа: "))
        r = int(input("Кількість кімнат: "))
        add_object(t, a, s, r)
        print("Об'єкт додано! ✅")

    elif choice == '2':
        oid = int(input("ID об'єкта: "))
        p = input("Призначення кімнати: ")
        a = float(input("Площа кімнати: "))
        add_room(oid, p, a)
        print("Кімнату додано! ✅")

    elif choice == '3':
        info = show_full_info()
        for row in info:
            print(row)

    elif choice == '4':
        t = input("Тип об'єкта: ")
        a = float(input("Мінімальна площа: "))
        results = filter_objects_by_type_and_area(t, a)
        for row in results:
            print(row)

    else:
        print("Невірний вибір ❌")
