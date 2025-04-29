from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import cgi
import os
from book_client import load_books, save_books, filter_books
def render_html(filename):
    path = os.path.join("template", filename)
    with open(path, encoding="utf-8") as f:
        return f.read()
def app(env, start_response):
    path = env.get("PATH_INFO", "")
    method = env["REQUEST_METHOD"]
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]
    if path == "/" or path == "/add":
        if method == "GET":
            body = render_html("add_book.html")
        elif method == "POST":
            form = cgi.FieldStorage(fp=env["wsgi.input"], environ=env)
            author = form.getfirst("author")
            title = form.getfirst("title")
            year = form.getfirst("year")
            books = load_books()
            books.append({"author": author, "title": title, "year": year})
            save_books(books)
            body = "<h3>Книгу додано!</h3><a href='/add'>Назад</a>"
    elif path == "/filter":
        body = render_html("filter_books.html")
    elif path == "/filter_result":
        qs = parse_qs(env.get("QUERY_STRING", ""))
        books = load_books()
        result = filter_books(
            books,
            author=qs.get("author", [""])[0],
            title=qs.get("title", [""])[0],
            year_from=qs.get("year_from", [""])[0],
            year_to=qs.get("year_to", [""])[0]
        )
        body = "<h2>Результати:</h2><ul>"
        for b in result:
            body += f"<li>{b['author']} – <em>{b['title']}</em> ({b['year']})</li>"
        body += "</ul><a href='/filter'>Назад</a>"
    else:
        status = "404 NOT FOUND"
        body = render_html("error_404.html")
    start_response(status, headers)
    return [body.encode("utf-8")]
if __name__ == "__main__":
    print("Сервер працює на http://localhost:8000")
    make_server("", 8000, app).serve_forever()