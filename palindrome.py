import cgi
from string import Template

def is_palindrome(string):
    s = ""
    for char in string:
        if char.isalpha():
            s += char.lower()
    return s == s[::-1]

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    answer = 'це паліндром!' if is_palindrome(string) else 'це не паліндром!'
    result = string + ' - ' + answer
    with open("2.html", encoding="utl-8") as f:
        page = Template(f.read()).substitute(result=result)
    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("unt-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n ")
    print(page)