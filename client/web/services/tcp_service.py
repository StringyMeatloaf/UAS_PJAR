from client.tcp_client.tcp_client import TCPClient


def upload_to_server(filepath):

    client = TCPClient()

    try:

        client.connect()

        return client.upload_file(filepath)

    except Exception as e:

        print(f"[TCP ERROR] {e}")

        return False

    finally:

        client.disconnect()