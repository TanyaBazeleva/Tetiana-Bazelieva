from urllib.request import urlopen  # Функція для отримання веб-сторінки з мережі
from urllib.parse import quote  # Функція для кодування кирилиці в url
from urllib.error import HTTPError  # Виключення, яке може виникнути при відповіді веб-сервера
from html.parser import HTMLParser  # Клас для аналізу HTML-файлу


class StationViewParser(HTMLParser):
    """ Клас, який дозволяє виконати аналіз html-файлу та знайти
    код експреса з заданою залізничною станцією.

    Щоб запустити пошук, потрібно викликати
    метод StationViewParser.feed(self, data),
    де data - дані з html-файлу.
    """

    def __init__(self, station):
        super().__init__()
        self.station = station  # Назва станції
        self.station_code = None  # Шуканий код станції
        self.entered_tr = False  # Чи увійшли в тег <tr>
        self.in_first_a = False  # Чи знаходимося в першому тегу <a>?
        self.found_a = False  # Чи знайшли тег <a> з шуканою назвою станції?
        self.td_count = 0  # Лічильник тегів <td>, які потрібно відрахувати щоб знайти потрібний
        self.in_code_td = False  # Чи знаходимося у потрібному полі з кодом станції?

    def handle_starttag(self, tag, attrs):
        """ Метод, який викликається,
        коли зустрічаємо відкриття тегу (<tag>).
        """
        if not self.station_code:
            # Якщо входимо в тег <tr>
            if tag == "tr":
                self.entered_tr = True
            # Якщо зустрічаємо перший тег <a> після <tr>
            elif self.entered_tr and tag == "a":
                self.in_first_a = True
            # Якщо знайшли потрібний тег <a>, починаємо відраховувати теги <td>
            elif self.found_a and tag == "td":
                # Якщо відрахували потрібну кількість тегів <td>,
                if self.td_count == 3:
                    self.in_code_td = True  # то знаходимося в потрібному тегу
                else:
                    self.td_count += 1

