import os

from shared.constants import BUFFER_SIZE, UPLOAD_FOLDER
from shared.protocol import *


def handle_upload(client):

    client.send(RESP_READY.encode(ENCODING))

    filename = client.recv(BUFFER_SIZE).decode(ENCODING)

    print(f"[FILENAME] {filename}")

    client.send(RESP_READY.encode(ENCODING))

    filesize = int(
        client.recv(BUFFER_SIZE).decode(ENCODING)
    )

    print(f"[FILESIZE] {filesize} bytes")

    client.send(RESP_READY.encode(ENCODING))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    received = 0

    with open(filepath, "wb") as file:

        while received < filesize:

            data = client.recv(BUFFER_SIZE)

            if not data:
                break

            file.write(data)

            received += len(data)

            progress = (received / filesize) * 100

            print(
            f"\rReceiving... {progress:.1f}% ",
            end=""
        )

    client.send(RESP_SUCCESS.encode(ENCODING))

    print("[UPLOAD COMPLETE]")