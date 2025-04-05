import json
import xml.etree.ElementTree as ET
JSON_FILE = "books.json"
XML_FILE = "books.xml"
def load_books():
    try:
        with open(JSON_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_books(books):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    save_books_to_xml(books)
def save_books_to_xml(books):
    root = ET.Element("books")
    for book in books:
        el = ET.SubElement(root, "book")
        for key, value in book.items():
            sub = ET.SubElement(el, key)
            sub.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
def filter_books(books, author=None, title=None, year_from=None, year_to=None):
    result = []
    for b in books:
        if author and author.lower() not in b["author"].lower():
            continue
        if title and title.lower() not in b["title"].lower():
            continue
        if year_from and int(b["year"]) < int(year_from):
            continue
        if year_to and int(b["year"]) > int(year_to):
            continue
        result.append(b)
    return result
