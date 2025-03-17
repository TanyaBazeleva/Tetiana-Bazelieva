# Використати структурний аналіз HTML за допомогою класу HTMLParser
# з модуля html.parser.

from urllib.request import urlopen  # функція для отримання веб-сторінки з мережі
from urllib.request import urlretrieve  # функція для завантаження файлу з мережі
from html.parser import HTMLParser
import os

class TopicsViewParser(HTMLParser):
    """ Клас для знаходження посилання на тему з номером n. """

    def __init__(self, n):
        super().__init__()
        self.topic = "Тема {}.".format(n)  # Номер теми
        self.in_a = False  # Чи знаходились в тегу <a>
        self.attrs = None  # Атрибути тегу
        self.url = None  # Посилання на веб-сторінку теми номер n

    def handle_starttag(self, tag, attrs):
        if not self.url:
            # Якщо знаходимось в тег <a> з класом "list-group-item"
            if tag == "a" and ("class", "list-group-item") in attrs:
                self.in_a = True
                self.attrs = attrs

    def handle_data(self, data):
        if not self.url:
            # Якщо знаходимось в тегу <a> та
            # його контент починається з рядка "Тема {}."
            if self.in_a and data.strip().startswith(self.topic):
                # Отримуємо атрибут з посиланням (href="...")
                self.url = dict(self.attrs)["href"]

    def handle_endtag(self, tag):
        if not self.url:
            # Якщо виходимо з тегу <a>
            if tag == "a":
                self.in_a = False


class PyFilesViewParser(HTMLParser):
    """ Клас для знаходження всіх python-файлів в html-документу. """

    def __init__(self):
        super().__init__()
        self.pyfiles = []  # Список знайдених python-файлів

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            # Якщо посилання закінчується на .py чи .pyw, то
            # додаємо його у список
            if href and href.endswith((".py", ".pyw")):
                self.pyfiles.append(href)


def get_html(url):
    """ Повертає розкодовані дані веб-сторінки за заданою адресою. """
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")


def download_examples(n, folder):
    """
    З сайту http://matfiz.univ.kiev.ua завантажує
    усі python-файли за номером теми n у директорію folder.
    """

    main_url = "http://matfiz.univ.kiev.ua"

    # Отримуємо дані веб-сторінки з темами
    topics_html = get_html(main_url + "/pages/13")

    # Шукаємо посилання на веб-сторінку з n-ю темою
    tvp = TopicsViewParser(n)
    tvp.feed(topics_html)
    topic_url = main_url + tvp.url

    # Отримуємо сторінку n-ого теми
    topic_html = get_html(topic_url)

    # Створюємо каталог для збереження файлів
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Знаходимо список відносних посилань на python-файли
    pfp = PyFilesViewParser()
    pfp.feed(topic_html)

    # Завантажуємо всі посилання на python-файли
    for example in pfp.pyfiles:
        filename = os.path.basename(example)  # Визначаємо ім'я файлу
        full_url = topic_url + example  # Формуємо повну URL-адресу
        urlretrieve(full_url, os.path.join(folder, filename))


if __name__ == "__main__":
    topic = 30
    download_examples(30, "python_files")
