# client/web/services/udp_service.py
from client.udp_client.udp_client import UDPClient

def stream_generator(filename):
    client = UDPClient()
    try:
        client.start_stream(filename)
        while True:
            frame_bytes = client.receive_frame()
            if frame_bytes is None:
                break
            if frame_bytes == b"":  # Skip jika sedang dalam fase timeout/pause
                continue
                
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes +
                b"\r\n"
            )
    finally:
        client.close()