from urllib.request import urlopen
import re
import os

STATION_CODE_PATTERN = r"(\d{7})"

def station(letter, name):
    url = f"https://uk.wikipedia.org/wiki/Список_залізничних_станцій_і_роз'їздів_України_({letter})"
    html = get_html(url)
    station_pattern = rf"{name}.*?{STATION_CODE_PATTERN}"
    match = re.search(station_pattern, html, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return "Станцію не знайдено"

def get_html(url):
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")

if __name__ == "__main__":
    letter = "К"
    name = "Київ-Пасажирський"
    code = station(letter, name)
