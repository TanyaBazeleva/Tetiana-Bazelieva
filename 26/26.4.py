import requests
from html.parser import HTMLParser

class DefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tag_p = False
        self.in_div = False
        self.current_result = ""
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ("class", "toggle-content") in attrs:
            self.in_div = True
        if self.in_div and tag == 'p':
            self.in_tag_p = True
            self.current_result += "\n"
    def handle_endtag(self, tag):
        if self.in_div and tag == 'div':
            self.in_div = False
    def handle_data(self, data):
        if self.in_tag_p:
            self.current_result += date


def get_definition(word: str) -> str:
    url = f"https://slovnyk.ua/?swrd= {word}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    if response.status_code != 200:
        return None
    else:
        return response.text

if __name__ == "__main__":
    word = "Галушки"
    print(get_definition(word), file=open('Галушка.txt', 'w'))
