import os
import socketserver
import shutil

BUFFER_SIZE = 4096
SEPARATOR = "_"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BACKUP_DIR = "backup_dir"

class BackupHandler(socketserver.BaseRequestHandler):
    def handle(self):
        command = self.request.recv(BUFFER_SIZE).decode()
        if command.startswith("SEND"):
            self.receive_backup(command)
        elif command.startswith("RECEIVE"):
            self.send_backup(command)

    def receive_backup(self, command):
        _, relative_path = command.split(SEPARATOR, 1)
        destination = os.path.join(BACKUP_DIR, relative_path)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as f:
            while True:
                data = self.request.recv(BUFFER_SIZE)
                if data.endswith(b"<END>"):
                    f.write(data[:-5])
                    break
                f.write(data)

    def send_backup(self, command):
        _, relative_path = command.split(SEPARATOR, 1)
        source = os.path.join(BACKUP_DIR, relative_path)
        if os.path.exists(source):
            if os.path.isfile(source):
                with open(source, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        self.request.sendall(chunk)
                self.request.sendall(b"<END>")
            elif os.path.isdir(source):
                for root, _, files in os.walk(source):
                    for file in files:
                        relative_file_path = os.path.relpath(os.path.join(root, file), BACKUP_DIR)
                        self.request.sendall(f"FILE{SEPARATOR}{relative_file_path}".encode() + b"<END>")
        else:
            self.request.sendall(b"NOT_FOUND")

if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with socketserver.TCPServer((SERVER_HOST, SERVER_PORT), BackupHandler) as server:
        print(f"{SERVER_HOST}:{SERVER_PORT}")
        server.serve_forever()
