from urllib.request import urlopen
from urllib.request import urlretrieve
import re
import os

PDFILE = r'"(.+\.pdf)"'
URL = "https://mp.mechmat.knu.ua/library"
def extract_between_h3(html, target = None):
    patern = re.compile(rf"<h3.*?>\s*{target}\s*</h3>(.*?)(?=<h3.*?>.*?</h3>|&)")
def dowlond_manual(n, folder, url, topics=None):
    topics_html = get_html(url)
    if not os.path.exists(folder):
        os.mkdir(folder)

    start = None
    for line in re.findall("<h3.*?>(.*?)</h3>", topics_html):
        print(line)
        if line == topics:
            start =
        topic_str = re.search(f"<h3.*?>{topics}</h3>", topics_html)
        print(topic_str)

    for example in re.findall(PDFILE, topics_html):
        example_url = url + example
        filename = os.path.basename(example)
        print(f" dowlonding {example_url} into {filename}")
        urlretrieve(example_url, os.path.join(folder, filename))

def get_html(url):
    return str(urlopen(url).read(), encoding = "utf-8", errno="ignore")

if __name__ == "__main__":
    topic = "Інформатика і програмування"
    dowlond_manual(f"manuals", URL, topics=topic)
