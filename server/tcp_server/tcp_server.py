import os
import sys
import socket

# =========================================================================
# FIX: Menambahkan root path proyek agar folder 'shared' bisa di-import di VM
# =========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))  # server/tcp_server
project_root = os.path.abspath(os.path.join(current_dir, "../../"))  # root proyek
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# =========================================================================

from shared.constants import TCP_PORT, BUFFER_SIZE
from shared.protocol import *

# Pastikan handler juga bisa mendeteksi imports dengan benar
from server.tcp_server.handlers import handle_upload

class TCPServer:

    def __init__(self):
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # Menggunakan "0.0.0.0" agar bisa diakses dari Windows
        self.server.bind(
            (
                "0.0.0.0",
                TCP_PORT
            )
        )

        self.server.listen(5)

        self.commands = {
            CMD_UPLOAD: handle_upload,
        }

        print(f"TCP Server Running and listening on port {TCP_PORT}...")

    def handle_client(self, client, addr):
        print(f"[CONNECTED] Connected from client: {addr}")
        try:
            command = client.recv(BUFFER_SIZE).decode(ENCODING)
            print(f"[COMMAND] Received command: {command}")

            handler = self.commands.get(command)

            if handler:
                handler(client)
            else:
                client.send(RESP_UNKNOWN.encode(ENCODING))
        except Exception as e:
            print(f"[SERVER ERROR] Error handling client {addr}: {e}")
        finally:
            client.close()
            print(f"[DISCONNECTED] Connection with {addr} closed.")

    def start(self):
        while True:
            try:
                # FIX: Hapus logic hasattr dan langsung gunakan accept() murni
                client, addr = self.server.accept()
                self.handle_client(client, addr)
            except Exception as e:
                print(f"[SERVER ERROR] Gagal menerima koneksi: {e}")
                continue


if __name__ == "__main__":
    server = TCPServer()
    server.start()