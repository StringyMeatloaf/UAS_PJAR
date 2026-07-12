# server/udp_server/handlers.py
import os
import cv2
import time

from shared.constants import UPLOAD_FOLDER, UDP_PACKET_SIZE
from shared.protocol import *

# Dictionary global untuk melacak status kontrol per client address
# Struktur data: { addr: "PLAYING" | "PAUSED" | "STOPPED" }
streaming_states = {}

def handle_stream(server, addr, filename):
    streaming_states[addr] = "PLAYING"
    error_count = 0 

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print(f"[STREAM] Memulai pengiriman ke {addr} -> {filepath}")

    if not os.path.exists(filepath):
        print(f"[ERROR] Video tidak ditemukan di path: {filepath}")
        server.sendto(RESP_ERROR.encode(ENCODING), addr)
        streaming_states.pop(addr, None)
        return

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        print("[ERROR] OpenCV gagal membuka file video.")
        server.sendto(RESP_ERROR.encode(ENCODING), addr)
        streaming_states.pop(addr, None)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    delay = 1 / fps
    print(f"[FPS DETECTED] Berjalan pada {fps} FPS (Delay: {delay:.4f}s)")

    while True:
        # 1. Antisipasi Perintah STOP
        if streaming_states.get(addr) == "STOPPED":
            print(f"[STREAM CONTROL] Perintah STOP diterima untuk {addr}.")
            server.sendto(RESP_END.encode(ENCODING), addr)
            break

        # 2. Antisipasi Perintah PAUSE
        if streaming_states.get(addr) == "PAUSED":
            time.sleep(0.1)  # Menahan loop agar tidak memakan CPU 100%
            continue

        # 3. Membaca Frame Video
        ret, frame = cap.read()
        if not ret:
            print(f"[STREAM FINISHED] Video selesai dikirim ke {addr}.")
            server.sendto(RESP_END.encode(ENCODING), addr)
            break

        # 4. Resize Frame untuk Kompresi Ukuran Data
        frame = cv2.resize(frame, (320, 180))

        # 5. Encode Gambar ke format JPEG dengan Kualitas Efisien
        success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 40])
        if not success:
            continue

        frame_bytes = buffer.tobytes()
        bytes_size = len(frame_bytes)

        # 6. Validasi Ukuran Buffer terhadap UDP_PACKET_SIZE
        if bytes_size > UDP_PACKET_SIZE:
            print(f"[WARNING] Frame dilewati! Ukuran ({bytes_size} bytes) melebihi batas.")
            continue

        # 7. Proses Pengiriman + Penanganan Timeout Otomatis (Jika Client Force Close)
        try:
            server.sendto(frame_bytes, addr)
            error_count = 0  
        except Exception as e:
            error_count += 1
            print(f"[ERROR] Gagal mengirim paket ke {addr} ({error_count}/5): {e}")
            if error_count >= 5:
                print(f"[STREAM TIMEOUT] Terlalu banyak kegagalan. Menghentikan stream untuk {addr}.")
                break 

        time.sleep(delay)

    cap.release()
    streaming_states.pop(addr, None)
    print(f"[INFO] Resource video untuk {addr} berhasil dibersihkan dari memori.")