import socket

from shared.constants import SERVER_IP, TCP_PORT, BUFFER_SIZE

from shared.protocol import *

from server.tcp_server.handlers import (
    handle_upload
)


class TCPServer:

    def __init__(self):

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.bind(
            (
                SERVER_IP,
                TCP_PORT
            )
        )

        self.server.listen(5)

        self.commands = {

            CMD_UPLOAD: handle_upload,

}

        print(f"TCP Server Running on {SERVER_IP}:{TCP_PORT}")

    def handle_client(self, client, addr):

        print(f"[CONNECTED] {addr}")

        command = client.recv(BUFFER_SIZE).decode(ENCODING)

        print(f"[COMMAND] {command}")

        handler = self.commands.get(command)

        if handler:

            handler(client)

        else:

            client.send(RESP_UNKNOWN.encode(ENCODING))

        client.close()

    def start(self):

        while True:

            client, addr = self.server.accept()

            self.handle_client(client, addr)


if __name__ == "__main__":

    server = TCPServer()

    server.start()