import socket
def symmetric(string):
    n = len(string)
    for i in range(1, n):
        left, right = string[:i], string[i:]
        if left == left[::-1] and right == right[::-1]:
            return True
    return False

HOST = ''
PORT = 20002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    data = conn.recv(1024)
    if not data: break
    string = str(data, encoding='utf-8')
    res = "Так, складається з двох симетричних підрядків.\n" if symmetric(string) else "Ні, не складається з двох симетричних підрядків.\n"
    conn.sendall(bytes(res, encoding='utf-8'))
conn.close()
