from urllib.request import urlopen  # Функція для отримання веб-сторінки з мережі
from urllib.request import Request  # Клас для формування запиту веб-клієнта
from urllib.parse import quote  # Функція для кодування виділеня в url
from urllib.error import HTTPError  # Оброблення, яке може виникнути при відповіді веб-сервера
from string import Template  # Клас для формування рядків
import re

# Шаблон для отримання опису тегу <tr>
TR_TAG = r"<tr>(.*?)<\/tr>"

# Шаблон для отримання експрес-коду станції
# Замість $station підставляється потрібна станція
CODE_PATTERN = r'<td><b><a.*?>$station<\/a><\/b><\/td>(?:\s*<td>.*?<\/td>){4}\s*<td>\s*?(?P<CODE>\d{1,7})\s*?<\/td>'


def get_station_code(station_name):
    """
    Повертає Код Експрес-3 заданої станції.

    :param station_name: назва станції
    :return: код станції
    """

    # Будуємо URL-запит
    url = "https://uk.wikipedia.org"
    path = "/wiki/Список_залізничних_станцій_і_роз'їздів_України_((" + station_name[0] + "))"

    # Кодуюмо запит в URL-значення
    full_url = url + quote(path, encoding="utf-8")

    request = Request(full_url, headers={})

    try:
        # Отримуємо веб-сторінку з мережі
        response = urlopen(request)

        # Розпізнаємо сторінку
        html = str(response.read(), encoding="utf-8", errors="ignore")

        # Шукаємо опис станції
        code_pattern = Template(CODE_PATTERN).substitute({"station": station_name})

        # Проходимо по всіх тегах <tr>
        for row_html in re.findall(TR_TAG, html, re.DOTALL):
            match = re.search(code_pattern, row_html, re.DOTALL)
            if match:
                # Якщо знайдено структуру виділення, друкуємо її значення
                return match.group("CODE")

    except HTTPError:
        return None

if __name__ == "__main__":
    stations = [
        "Київ-Пасажирський",
        "Львів",
        "Київ",
        "Орліщина"
    ]

    for station in stations:
        code = get_station_code(station)
        if code:
            print(station, ":", code)
        else:
            print(station, ": Код не знайдено")
