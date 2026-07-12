# client/udp_client/udp_client.py
import socket
from shared.constants import SERVER_IP, UDP_PORT, UDP_BUFFER_SIZE
from shared.protocol import *

class UDPClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.settimeout(3.0)  # Cegah Flask hang selamanya jika server UDP mati
        self.server_address = (SERVER_IP, UDP_PORT)

    def start_stream(self, filename):
        request = f"{CMD_STREAM}|{filename}"
        self.client.sendto(request.encode(ENCODING), self.server_address)

    def receive_frame(self):
        try:
            frame_bytes, _ = self.client.recvfrom(UDP_BUFFER_SIZE)
            if frame_bytes in [RESP_ERROR.encode(ENCODING), RESP_END.encode(ENCODING)]:
                return None
            return frame_bytes
        except socket.timeout:
            return b""  # Kembalikan byte kosong saat ter-pause (server tidak kirim data)
        except Exception:
            return None

    def close(self):
        self.client.close()