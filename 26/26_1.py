from urllib.request import urlopen, urlretrieve
import re
import os

# Шаблон для знаходження PDF-файлів
PDFFILE = r'href="(.+?\.pdf)"'

def download_pdfs(url, folder):
    """ Завантажує всі PDF-файли з вказаної веб-сторінки у вказану папку. """
    # Отримуємо HTML-код сторінки
    html = get_html(url)

    # Створюємо каталог для збереження файлів, якщо його немає
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Знаходимо всі посилання на PDF-файли
    pdf_links = re.findall(PDFFILE, html)
    base_url = "https://mp.mechmat.kmu.ua"

    for pdf_link in pdf_links:
        full_url = pdf_link if pdf_link.startswith("http") else base_url + pdf_link
        filename = os.path.basename(pdf_link)

        # Завантажуємо PDF-файл
        print(f"Завантаження {full_url}")
        urlretrieve(full_url, os.path.join(folder, filename))

    print("Завантаження завершено.")

def get_html(url):
    """ Повертає розкодовні дані веб-сторінки за заданою адресою. """
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")

if __name__ == "__main__":
    download_pdfs("https://mp.mechmat.kmu.ua/library", "pdf_files")
