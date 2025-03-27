import xml.etree.ElementTree as Et
import cgi
from string import Template
from wsgiref.simple_server import make_server

OPTION = """
<option value="$cur_id">$cur_name</option>
"""

class ExchangeRateXML:
    def __init__(self, data):
        self.data = data
    def get_currencies(self):
        """Повертає список валют з файлу XML"""
        etree = Et.parse(self.data)
        currencies_el = etree.find("currencies")
        currencies = []
        for currency_el in currencies_el:
            currency = (
                currency_el.get("id"),
                currency_el.text.strip()
            )
            currencies.append(currency)
        return currencies

    def obtain_rate(self, cur1_id, cur2_id, amount):
        if cur1_id == cur2_id:
            return amount
        etree = Et.parse(self.data)
        xpath = "exchange_rates/rate[@currency1='{}'][@currency2='{}']"
        rate_el = etree.find(xpath.format(cur1_id, cur2_id))
        if rate_el is not None:
            rate = float(rate_el.text)
            return amount / rate
        rate_el = etree.find(xpath.format(cur2_id, cur1_id))
        if rate_el is not None:
            rate = float(rate_el.text)
            return amount * rate

        return None

    def get_currency_name(self, currency_id):
        """Повертає ім’я валюти згідно її id"""
        etree = Et.parse(self.data)
        xpath = f"currencies/currency[@id='{currency_id}']"
        currency_el = etree.find(xpath)
        return currency_el.text

    def create_xml(self, cur1_id, cur2_id, amount, filename):
        """
        Створює XML-файл з відповіддю для конвертування amount
        грошей у валюті cur1 до валюти cur2
        """
        rate = round(self.obtain_rate(cur1_id, cur2_id, amount), 2)
        cur1_name = self.get_currency_name(cur1_id)
        cur2_name = self.get_currency_name(cur2_id)

        root = Et.Element("exchange_rate")

        cur_el = Et.Element("currency", {"id": cur1_id, "name": cur1_name})
        cur_el.text = str(amount)
        root.append(cur_el)

        cur_el = Et.Element("currency", {"id": cur2_id, "name": cur2_name})
        cur_el.text = str(rate)
        root.append(cur_el)

        tree = Et.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def __call__(self, environ, start_response):
        """Обробка HTTP-запиту"""
        headers = [('Content-type', 'text/html; charset=utf-8')]
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        path = environ.get('PATH_INFO', '').lstrip('/')
        params = {'currencies': ''}

        if path == "":
            for cur_id, cur_name in self.get_currencies():
                params['currencies'] += Template(OPTION).substitute(cur_id=cur_id, cur_name=cur_name)

            with open("templates/currencies.html", encoding="utf-8") as f:
                page = Template(f.read())
                html = page.substitute(params)
                start_response("200 OK", headers)
                return [bytes(html, encoding="utf-8")]

        elif path == "exchange_rate.xml":
            cur1 = form.getfirst("from")
            cur2 = form.getfirst("to")
            amount = float(form.getfirst("amount"))
            self.create_xml(cur1, cur2, amount, "exchange_rate.xml")

            with open("exchange_rate.xml", encoding="utf-8") as f:
                xml = f.read()
                start_response("200 OK", [('Content-type', 'application/xml; charset=utf-8')])
                return [bytes(xml, encoding="utf-8")]

        else:
            status = "404 NOT FOUND"
            file = "templates/error_404.html"
            start_response(status, headers)

            with open(file, encoding="utf-8") as f:
                page = Template(f.read()).substitute()
                return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == "__main__":
    app = ExchangeRateXML("data/currencies.xml")
    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, app).serve_forever()
