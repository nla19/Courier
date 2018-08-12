import socket
import sys


class FTPClient:
    def __init__(self, serverHost, serverPort):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.socket = None

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            # TODO: Added exit
            sys.exit(1)

    def socket_connect(self):
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except socket.error as msg:
            print("Socket connection error: " + str(msg))

    # Send request to server
    def request(self, payload):
        try:
            payload = payload.encode()
        except AttributeError:
            pass

        self.socket.send(payload)

    def socket_close(self):
        try:
            self.socket.close()
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()


if __name__ == "__main__":
    client = FTPClient("192.168.56.101", 50007)
    client.socket_create()
    client.socket_connect()
    try:
        while True:
            request = input("192.168.1.8>")
            client.request(bytes(request, "utf-8"))
            if request == 'exit':
                break
    except KeyboardInterrupt:
        client.socket_close()
        sys.exit()
    except IOError as bp:
        client.socket.close()
        print("Connection closed by peer ({})".format(client.serverHost))
