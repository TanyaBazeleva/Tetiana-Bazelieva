import os
import socket

BUFFER_SIZE = 4096
SEPARATOR = "_"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001

def receive_backup(destination):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    s.sendall(f"RECEIVE{SEPARATOR}".encode())
    while True:
        data = s.recv(BUFFER_SIZE)
        if data == b"NOT_FOUND":
            print("Резервні копії не знайдено")
            break
        elif data.endswith(b"<END>"):
            data = data[:-5]
            relative_path, file_content = data.split(SEPARATOR.encode(), 1)
            file_path = os.path.join(destination, relative_path.decode())
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file_content)
        else:
            relative_path = data.decode()
            print(f"Отримано файл: {relative_path}")
    s.close()

if __name__ == "__main__":
    destination = input(" ")
    receive_backup(destination)
