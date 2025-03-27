import socket
import xml.etree.ElementTree as ET

# Дані про погоду
weather_data = {
    "Київ": {"temperature": "15", "condition": "Сонячно"},
    "Львів": {"temperature": "10", "condition": "Дощ"},
    "Одеса": {"temperature": "20", "condition": "Хмарно"},
}

def handle_request(xml_request):
    """Обробляє XML-запит клієнта та формує відповідь у XML"""
    root = ET.fromstring(xml_request)
    city = root.find("city").text

    response = ET.Element("response")
    ET.SubElement(response, "city").text = city

    if city in weather_data:
        ET.SubElement(response, "temperature").text = weather_data[city]["temperature"]
        ET.SubElement(response, "condition").text = weather_data[city]["condition"]
    else:
        ET.SubElement(response, "error").text = "Місто не знайдено"

    return ET.tostring(response, encoding="utf-8").decode()


# Запускаємо сервер
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 65432))
server.listen(1)
print("Сервер запущено, очікуємо з'єднання...")

while True:
    conn, addr = server.accept()
    print(f"Підключився клієнт: {addr}")

    data = conn.recv(1024).decode()
    if not data:
        break

    response_xml = handle_request(data)
    conn.send(response_xml.encode())

    conn.close()
