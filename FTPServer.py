import socket
import sys
import time


class FTPServer:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.socket = None
        self.connection = None
        self.addr = None

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            sys.exit(1)

    def socket_bind(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            print("Socket binding error: " + str(e))
            time.sleep(5)
            self.socket_bind()

    def socket_accept(self):
        try:
            conn, addr = self.socket.accept()
            self.connection = conn
            self.addr = addr
            print("Connection from {}".format(addr[0]))
        except socket.error as msg:
            print("Socket accept error: " + str(msg))

    def receive(self):
        data = self.connection.recv(65536)
        print("Received {} bytes from {}: {}".format(len(data), self.addr[0], data))
        return data

    def socket_close(self):
        try:
            self.socket.close()
            self.connection = None
            self.addr = None
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()


if __name__ == "__main__":
    server = FTPServer(50007)
    server.socket_create()
    server.socket_bind()
    server.socket_accept()
    data = None
    try:
        while True and data != b'exit':
            data = server.receive()
    except KeyboardInterrupt:
        server.socket_close()
        sys.exit()
