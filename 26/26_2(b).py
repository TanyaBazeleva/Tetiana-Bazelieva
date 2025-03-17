from urllib.request import urlopen
from html.parser import HTMLParser

class StationParser(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.in_row = False
        self.station_code = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = False
        if tag == "td" and self.name in dict(attrs).get("class", ""):
            self.in_row = True

    def handle_data(self, data):
        if self.in_row and data.strip().isdigit() and len(data.strip()) == 7:
            self.station_code = data.strip()

    def handle_endtag(self, tag):
        if tag == "tr":
            self.in_row = False


def get_html(url):
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")


def station(letter, name):
    url = f"https://uk.wikipedia.org/wiki/Список_залізничних_станцій_і_роз'їздів_України_({letter})"
    html = get_html(url)
    parser = StationParser(name)
    parser.feed(html)
    return parser.station_code or "Станцію не знайдено"


if __name__ == "__main__":
    letter = "К"
    name = "Київ-Пасажирський"
    code = station(letter, name)
