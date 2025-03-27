import socket
import xml.etree.ElementTree as ET

def create_request(city):
    """Створює XML-запит про погоду для сервера"""
    request = ET.Element("request")
    ET.SubElement(request, "city").text = city
    return ET.tostring(request, encoding="utf-8").decode()

# Ввід користувача
city = input("Введіть назву міста: ")

# Підключення до сервера
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 65432))

# Надсилаємо XML-запит
request_xml = create_request(city)
client.send(request_xml.encode())

# Отримуємо XML-відповідь
response_xml = client.recv(1024).decode()
client.close()

# Обробка відповіді
root = ET.fromstring(response_xml)
if root.find("error") is not None:
    print(f"Помилка: {root.find('error').text}")
else:
    print(f"Погода в {root.find('city').text}: {root.find('temperature').text}°C, {root.find('condition').text}")
