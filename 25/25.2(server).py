import socketserver

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        s = self.get_line()
        res = self.perevir(s)
        self.request.sendall(res.encode())

    def perevir(self, j):
        try:
            return str(eval(j, {"__builtins__": None}, {}))
        except:
            return "Некоректний вираз"

    def get_line(self):
        buf = bytes()
        while '\n' not in buf.decode():
            buf += self.request.recv(1)
        buf = buf.decode().strip()
        print(buf)
        return buf

HOST = '127.0.0.1'
PORT = 1234

if __name__ == '__main__':
    print('=== server start ===')
    socketserver.TCPServer((HOST, PORT), RequestHandler).serve_forever()