from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import os
from xml_client import get_works_by_site
def render_html(filename):
    path = os.path.join("templates", filename)
    with open(path, encoding="utf-8") as f:
        return f.read()
def app(env, start_response):
    path = env.get("PATH_INFO", "")
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]
    if path in ("/", "/form"):
        body = render_html("form.html")
    elif path == "/result":
        qs = parse_qs(env.get("QUERY_STRING", ""))
        site_id = qs.get("site_id", [""])[0]
        works = get_works_by_site(site_id)
        body = f"<h2>Роботи для майданчику {site_id}</h2><ul>"
        for w in works:
            body += f"<li>{w}</li>"
        body += "</ul><a href='/form'>Назад</a>"
    else:
        status = "404 NOT FOUND"
        body = render_html("error_404.html")
    start_response(status, headers)
    return [body.encode("utf-8")]
if __name__ == "__main__":
    print("Сервер працює на http://localhost:8000")
    make_server("", 8000, app).serve_forever()
