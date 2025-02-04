import socket

HOST = '127.0.0.1'
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

filename = "25_2.txt"

with open(filename, 'r') as f1:
    with open('25_2(result).txt', 'w') as f2:
        dts = f1.readlines()
        for dt in dts:
            s.sendall(bytes(dt.strip() + '\n', encoding='utf-8'))
            result = s.recv(1024)
            f2.write(dt.strip() + " = " + result.decode() + '\n')

s.close()
