import cgi, json
from wsgiref.simple_server import make_server

def separate(a):
    b = []
    sp = a.split()
    for i in sp:
        if i not in b:
            b.append(i)
    return b

def res1(a):
    words = separate(a)
    c = json.dumps(words, ensure_ascii=False)
    with open("words.json", "w") as f:
        json.dump(words, f)
    return c

def application(environ, start_response):
    if environ.get('PATH_INFO', '').lstrip('/') == '28_1.py':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if 'a' in form:
            a = form['a'].value
            start_response('200 OK', [('Content-Type', 'application/json')])
            body = res1(a)
            return [bytes(body, encoding='utf-8')]

        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            body = 'Сторінку не знайдено'
            return [bytes(body, encoding='utf-8')]

print("-----Сервер почав роботу-----")
httpd = make_server("localhost", 8000, application)
httpd.serve_forever()
