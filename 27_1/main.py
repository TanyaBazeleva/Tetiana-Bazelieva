import cgi
from string import Template

def is_palindrome(string):
    s = ""
    for char in string:
        if char.isalpha():
            s += char.lower()
    return s == s[::-1]

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        if string == "":
            result = ""
        else:
            answer = "це паліндром" if is_palindrome(string) else "це не паліндром"
            result = "<h1>{} - {}<h1>".format(string, answer)
        start_response("200 ОК", [("content-type", "text/html; charset-utf-8"), ])
        with open("template/palindrome.html", encoding="utf-8") as f:
            content = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND",[("Content-type", "text/html; charset-utf-8"), ])
        with open("template/error_404.html", encoding="utf-8") as f:
            content = f.read()
    return [bytes(content, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server(HOST, PORT, application)
    print(f"Local webserver is running at http://localhost:{PORT}")
    httpd.serve_forever()