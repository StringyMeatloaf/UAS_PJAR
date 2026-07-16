import socket
import os
import time
import sys

# Menambahkan root path proyek agar folder 'shared' bisa di-import di VM Linux
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from shared.constants import UDP_PORT, UDP_PACKET_SIZE, UPLOAD_FOLDER
from shared.protocol import ENCODING

HOST = "0.0.0.0"  # Mendengarkan koneksi dari luar VM (Windows)
PORT = UDP_PORT   # Menggunakan port dari constants (5002)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Memperbesar buffer sistem operasi agar tidak ada paket loss di network
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
server.bind((HOST, PORT))

print(f"UDP Server berjalan di {HOST}:{PORT}")

while True:
    try:
        # 1. Menerima request nama file dari Flask Client
        data, address = server.recvfrom(1024)
        filename = data.decode(ENCODING)

        # Saring jika ada instruksi kontrol liar dari sisa kode lama
        if filename in ["PAUSE", "PLAY", "STOP"]:
            continue

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print(f"\n[REQUEST] Client {address} meminta video: {filename}")

        # 2. Validasi Keberadaan File
        if not os.path.exists(filepath):
            server.sendto(b"NOT_FOUND", address)
            print("[ERROR] File tidak ditemukan.")
            continue

        # 3. Kirim Ukuran File (Filesize)
        filesize = os.path.getsize(filepath)
        server.sendto(str(filesize).encode(ENCODING), address)

        # 4. Menunggu ACK 'READY' dari Flask Client
        ack, _ = server.recvfrom(1024)
        if ack != b"READY":
            print("[CANCEL] Client belum siap. Membatalkan streaming.")
            continue

        print(f"[STREAMING] Mulai mengirim data biner ke {address}...")

        # 5. Loop Pengiriman Byte Mentah (Raw Byte Chunk Streaming)
        with open(filepath, "rb") as video:
            sent = 0
            while True:
                chunk = video.read(UDP_PACKET_SIZE) # Menggunakan BUFFER_SIZE 60000
                if not chunk:
                    break

                server.sendto(chunk, address)
                sent += len(chunk)

                percent = (sent / filesize) * 100
                print(f"\rProgress Pengiriman : {percent:.2f}%", end="")

                # Jeda mikro agar kartu jaringan client tidak kebanjiran paket data
                time.sleep(0.002)

        # 6. Kirim Sinyal Penutup Video
        server.sendto(b"END_VIDEO", address)
        print("\n[SUCCESS] Streaming selesai ditransmisikan.")

    except Exception as e:
        print(f"\n[SERVER ERROR] Terjadi kendala: {e}")
        continue