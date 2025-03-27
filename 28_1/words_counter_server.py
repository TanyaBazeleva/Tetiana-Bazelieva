from words_counter_client import words_counter_from_url_to_json
import cgi

def app(environ, start_response):
    path = environ.get("PATH_INFO", "").lstrip("/")
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]
    file = "templates/words_count.html"
    # http://127.0.0.1:8000/
    if path == "":
        pass
    # http://127.0.0.1:8000/words_count.json
    elif path == "words_count.json":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        url = form.getfirst("url", "")

        if url:
            file = "data/words_count.json"
            words_counter_from_url_to_json(url, file)
            headers[0] = ("Content-Type", "text/json; charset=utf-8")
        else:
            status = "303 SEE OTHER"
            headers.append(("Location", "/"))
    # http://127.0.0.1:8000/<будь-який інший запит>
    else:
        status = "404 NOT FOUND"
        file = "templates/error_404.html"

    start_response(status, headers)
    with open(file, encoding="utf-8") as f:
        page = f.read()
    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    print("=== Local webserver ===")
    make_server(HOST, PORT, app).serve_forever()