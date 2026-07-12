# server/udp_server/udp_server.py
import socket
import threading

from shared.constants import SERVER_IP, UDP_PORT, UDP_BUFFER_SIZE
from shared.protocol import *
from server.udp_server.handlers import handle_stream, streaming_states

class UDPServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((SERVER_IP, UDP_PORT))
        print(f"UDP Server Running on {SERVER_IP}:{UDP_PORT}")

    def handle_client(self, data, addr):
        try:
            message = data.decode(ENCODING)
            parts = message.split("|")
            command = parts[0]
            filename = parts[1] if len(parts) > 1 else None

            print(f"[CLIENT COMMAND] {command} dari {addr}")

            if command == CMD_STREAM:
                # Jalankan pengiriman video di thread baru (Non-blocking)
                client_thread = threading.Thread(
                    target=handle_stream,
                    args=(self.server, addr, filename)
                )
                client_thread.daemon = True  
                client_thread.start()
                
            elif command == "PAUSE":
                streaming_states[addr] = "PAUSED"
                print(f"[CONTROL] {addr} status: PAUSED")
                
            elif command == "PLAY":
                streaming_states[addr] = "PLAYING"
                print(f"[CONTROL] {addr} status: RESUME/PLAYING")
                
            elif command == "STOP":
                streaming_states[addr] = "STOPPED"
                print(f"[CONTROL] {addr} status: STOPPED")
                
            else:
                self.server.sendto(RESP_UNKNOWN.encode(ENCODING), addr)
        except Exception as e:
            print(f"[ERROR] Gagal memproses data dari client {addr}: {e}")

    def start(self):
        while True:
            try:
                data, addr = self.server.recvfrom(UDP_BUFFER_SIZE)
                self.handle_client(data, addr)
            except Exception as e:
                print(f"[SERVER CRASH PREVENTION] Socket utama error: {e}")
                continue

if __name__ == "__main__":
    server = UDPServer()
    server.start()