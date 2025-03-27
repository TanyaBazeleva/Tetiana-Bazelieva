import re
from collections import Counter
from urllib.request import urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser
import xml.etree.ElementTree as et

WORD = r'\w+'  # Шаблон для пошуку слів

class WordsCounterHTMLParser(HTMLParser):
    """Клас для аналізу HTML і підрахунку слів."""
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.in_script = False
        self.counter = Counter()

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        elif tag == "script":
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_body and not self.in_script:
            words = re.findall(WORD, data, re.I)
            words = [word.lower() for word in words]
            self.counter.update(words)

def words_counter(string: str) -> Counter:
    """Рахує кількість слів у рядку."""
    words = re.findall(WORD, string, re.I)
    words = [word.lower() for word in words]
    return Counter(words)

def words_counter_to_xml(counter: Counter, filename: str):
    """Зберігає результат у XML-файл."""
    words_el = et.Element("words")
    for word in sorted(counter):
        word_el = et.Element("word")
        word_el.set("count", str(counter[word]))
        word_el.text = word
        words_el.append(word_el)
    etree = et.ElementTree(words_el)
    etree.write(filename, encoding="utf-8", xml_declaration=True)

def words_counter_from_url_to_xml(url: str, filename: str):
    """Читає слова з URL, рахує і зберігає в XML."""
    try:
        request = urlopen(url)
        data = str(request.read(), encoding="utf-8", errors="ignore")
        info = request.info()
        if info.get("Content-type", "").startswith("text/html"):
            wc = WordsCounterHTMLParser()
            wc.feed(data)
            counter = wc.counter
        else:
            counter = words_counter(data)

        words_counter_to_xml(counter, filename)
    except HTTPError as e:
        print(e)

if __name__ == "__main__":
    test_data = [
        "http://matfiz.univ.kiev.ua/pages/15",
        "http://matfiz.univ.kiev.ua/userfiles/files/t01_01_polynom.py",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"
    ]

    for i, url in enumerate(test_data, 1):
        filename = "data/test{}.xml".format(i)
        words_counter_from_url_to_xml(url, filename)
