from string import Template
import cgi

def count_sign_changes(sequence):
    nums = list(map(int, sequence.split(',')))
    sign_changes = 0
    for i in range(len(nums) - 1):
        if nums[i] * nums[i + 1] < 0:
            sign_changes += 1
    return sign_changes

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        sequence = form.getfirst("sequence", "")
        if sequence == "":
            result = ""
        else:
            try:
                changes = count_sign_changes(sequence)
                result = f"<h1>Кількість змін знаку - {changes}</h1>"
            except ValueError:
                result = "<h1>Помилка: Введіть коректну послідовність цілих чисел через кому.</h1>"
        start_response("200 OK", [("content-type", "text/html; charset=utf-8")])
        with open("template/sequence.html", encoding="utf-8") as f:
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
