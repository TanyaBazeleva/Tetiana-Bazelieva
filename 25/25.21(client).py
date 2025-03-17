import socket
HOST = 'localhost'
PORT = 20002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    to_send = input('?: ')
    if not to_send: break
    s.sendall(bytes(to_send, encoding='utf-8'))
    data = s.recv(1024)
    response = str(data, encoding='utf-8').strip()
    print(f'{to_send} - {response}')
s.close()
