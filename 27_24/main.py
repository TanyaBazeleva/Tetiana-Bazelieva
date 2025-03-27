from string import Template
import pandas as pd
import cgi

def calculate_score(price, p_max, rating, r_max, a1, a2):
    return a1 * price / p_max + a2 * rating / r_max

def get_best_supplier(file_path, products, a1, a2):
    suppliers = pd.read_excel(file_path, sheet_name="Постачальники")
    prices = pd.read_excel(file_path, sheet_name="Ціна")
    r_max = suppliers['Rating'].max()
    best_suppliers = []
    for product in products:
        product_prices = prices[prices['P_id'] == product]
        p_max = product_prices['Price'].max()
        best_score = -1
        best_supplier = None
        for _, row in product_prices.iterrows():
            supplier = suppliers[suppliers['Id'] == row['S_id']].iloc[0]
            score = calculate_score(row['Price'], p_max, supplier['Rating'], r_max, a1, a2)
            if score > best_score:
                best_score = score
                best_supplier = {
                    "Product": product,
                    "Supplier": supplier['Name'],
                    "Price": row['Price'],
                    "Term": row['Term'],
                    "Score": round(best_score, 2)
                }
        if best_supplier:
            best_suppliers.append(best_supplier)

    return best_suppliers

def application(environ, start_response):
    path = environ.get("PATH_INFO", "").lstrip("/")
    if path == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        products = form.getlist("products")
        a1 = float(form.getfirst("a1", "0.5"))
        a2 = float(form.getfirst("a2", "0.5"))
        result = ""

        if products and a1 + a2 == 1:
            best_suppliers = get_best_supplier("data.xlsx", products, a1, a2)
            rows = ""
            for supplier in best_suppliers:
                rows += f"<tr><td>{supplier['Product']}</td><td>{supplier['Supplier']}</td><td>{supplier['Price']}</td><td>{supplier['Term']}</td><td>{supplier['Score']}</td></tr>"
            result = f"<table border='1'><tr><th>Товар</th><th>Постачальник</th><th>Ціна</th><th>Термін</th><th>Оцінка</th></tr>{rows}</table>"
        else:
            result = "<h1>Помилка: Некоректні коефіцієнти або список товарів.</h1>"

        start_response("200 OK", [("content-type", "text/html; charset=utf-8")])
        with open("template/tender.html", encoding="utf-8") as f:
            content = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("template/error_404.html", encoding="utf-8") as f:
            content = f.read()
    return [bytes(content, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server(HOST, PORT, application)
    print(f"Local webserver is running at http://localhost:{PORT}")
    httpd.serve_forever()