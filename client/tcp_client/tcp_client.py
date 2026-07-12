import os
import socket

from shared.constants import (
    SERVER_IP,
    TCP_PORT,
    BUFFER_SIZE
)

from shared.protocol import *


class TCPClient:

    def __init__(self):

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    # =====================================================
    # Connect
    # =====================================================
    def connect(self):

        self.client.connect(
            (
                SERVER_IP,
                TCP_PORT
            )
        )

        print(f"[CONNECTED] {SERVER_IP}:{TCP_PORT}")

    # =====================================================
    # Send Command
    # =====================================================
    def send_command(self, command):

        self.client.send(
            command.encode(ENCODING)
        )

        response = self.client.recv(
            BUFFER_SIZE
        ).decode(ENCODING)

        print(f"[SERVER] {response}")

        return response

    # =====================================================
    # Upload File
    # =====================================================
    def upload_file(self, filepath):

        try:

            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)

            # -------------------------------
            # Send Upload Command
            # -------------------------------
            self.client.send(
                CMD_UPLOAD.encode(ENCODING)
            )

            response = self.client.recv(
                BUFFER_SIZE
            ).decode(ENCODING)

            print(f"[SERVER] {response}")

            if response != RESP_READY:
                return False

            # -------------------------------
            # Send Filename
            # -------------------------------
            self.client.send(
                filename.encode(ENCODING)
            )

            response = self.client.recv(
                BUFFER_SIZE
            ).decode(ENCODING)

            print(f"[SERVER] {response}")

            if response != RESP_READY:
                return False

            # -------------------------------
            # Send Filesize
            # -------------------------------
            self.client.send(
                str(filesize).encode(ENCODING)
            )

            response = self.client.recv(
                BUFFER_SIZE
            ).decode(ENCODING)

            print(f"[SERVER] {response}")

            if response != RESP_READY:
                return False

            # -------------------------------
            # Send File
            # -------------------------------
            with open(filepath, "rb") as file:

                while True:

                    data = file.read(BUFFER_SIZE)

                    if not data:
                        break

                    self.client.sendall(data)

            # -------------------------------
            # Upload Result
            # -------------------------------
            response = self.client.recv(
                BUFFER_SIZE
            ).decode(ENCODING)

            print(f"[SERVER] {response}")

            return response == RESP_SUCCESS

        except Exception as e:

            print(f"[UPLOAD ERROR] {e}")

            return False

    # =====================================================
    # Disconnect
    # =====================================================
    def disconnect(self):

        self.client.close()

        print("[DISCONNECTED]")


if __name__ == "__main__":

    client = TCPClient()

    client.connect()

    success = client.upload_file("sample.mp4")

    print(f"Upload Success : {success}")

    client.disconnect() 