import socket
from shared.constants import SERVER_IP, UDP_PORT, UDP_BUFFER_SIZE, UDP_PACKET_SIZE
from shared.protocol import ENCODING

def stream_generator(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5.0)  # Timeout jika server mati mendadak
    server_address = (SERVER_IP, UDP_PORT)

    try:
        # 1. Kirim request nama file ke VM Server
        client.sendto(filename.encode(ENCODING), server_address)
        
        # 2. Terima respon ukuran file / status
        try:
            response, _ = client.recvfrom(1024)
        except socket.timeout:
            print("[CLIENT] Gagal terhubung ke UDP Server (Timeout)")
            return

        if response == b"NOT_FOUND":
            print("[CLIENT] Video tidak ditemukan di server.")
            return
            
        filesize = int(response.decode(ENCODING))
        print(f"[CLIENT] Menghubungkan... Ukuran file target: {filesize} bytes")

        # 3. Kirim balik sinyal READY ke server
        client.sendto(b"READY", server_address)

        # 4. Loop menerima chunk data video mentah
        while True:
            try:
                # Menggunakan UDP_BUFFER_SIZE (65507) agar muat menampung packet 60000 bytes
                chunk, _ = client.recvfrom(UDP_BUFFER_SIZE)
                
                if chunk == b"END_VIDEO":
                    print("[CLIENT] Sinyal END_VIDEO diterima.")
                    break
                    
                # Hasilkan raw chunk stream langsung ke browser
                yield chunk
                
            except socket.timeout:
                print("[CLIENT] Koneksi timeout saat menerima data video.")
                break
                
    finally:
        client.close()
        print("[CLIENT] Socket streaming ditutup.")