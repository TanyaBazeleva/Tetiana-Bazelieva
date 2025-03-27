import xml.etree.ElementTree as ET

# Зчитування XML-файлу
tree = ET.parse("books.xml")
root = tree.getroot()

# Виведення назв книг та авторів
for book in root.findall("book"):
    title = book.find("title").text
    author = book.find("author").text
    print(f"Книга: {title}, Автор: {author}")

# Додавання нової книги
new_book = ET.Element("book")
ET.SubElement(new_book, "title").text = "1984"
ET.SubElement(new_book, "author").text = "Джордж Орвелл"
ET.SubElement(new_book, "year").text = "1949"

# Додаємо до бібліотеки та зберігаємо
root.append(new_book)
tree.write("books.xml", encoding="utf-8", xml_declaration=True)
