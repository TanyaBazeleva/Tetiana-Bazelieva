import re
from collections import Counter
from urllib.request import urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser
import json

WORD = r'\b([a-zа-яієґ\'’]+)\b'  # Додано підтримку апострофа

class WordsCounterHTMLParser(HTMLParser):
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

    def handle_data(self, data):  # ← Було помилково "date"
        if self.in_body and not self.in_script:
            words = re.findall(WORD, data, re.I)
            words = [word.lower() for word in words]
            self.counter.update(words)

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

def words_counter(data: str) -> Counter:
    words = re.findall(WORD, data, re.I)
    words = [word.lower() for word in words]
    return Counter(words)

def words_counter_to_json(counter: Counter, filename: str):
    lst = [
        {"word": word, "count": counter[word]}
        for word in sorted(counter)
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(lst, f, indent=4, ensure_ascii=False)

def words_counter_from_url_to_json(url: str, filename: str):
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

        words_counter_to_json(counter, filename)
    except HTTPError as e:
        print(e)

if __name__ == "__main__":
    test_data = [
        "http://matfiz.univ.kiev.ua/pages/15",
        "http://matfiz.univ.kiev.ua/userfiles/files/t01_01_polynom.py",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"
    ]

    for i, url in enumerate(test_data, 1):
        filename = "data/test{}.json".format(i)
        words_counter_from_url_to_json(url, filename)
