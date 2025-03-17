import os
import socket

BUFFER_SIZE = 4096
SEPARATOR = "_"

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001

def send_backup(directory):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            s.sendall(f"SEND{SEPARATOR}{relative_path}".encode())
            with open(file_path, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
            s.sendall(b"<END>")
    s.close()

if __name__ == "__main__":
    directory = input(" ")
    send_backup(directory)
