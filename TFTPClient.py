#   Author: Nick Abbott     Date: 08-11-18
#   Description: This file is my python 3 implementation of a TFTP client.
#                My motivation for this project was to better understand TFTP
#                and practice my programming skills. I realize this is re-inventing
#                the wheel, but it was fun, good practice, and educational
#                (concerning TFTP and UDP sockets).
#
#   Documentation from RFC 1350: Trivial File Transfer Protocol
#
#                       Figure 5-1: RRQ/WRQ packet
#
#            2 bytes     string    1 byte     string   1 byte
#            ------------------------------------------------
#           | Opcode |  Filename  |   0  |    Mode    |   0  |
#            ------------------------------------------------
#
#                       Figure 5-2: DATA packet
#
#                   2 bytes     2 bytes      n bytes
#                   ----------------------------------
#                  | Opcode |   Block #  |   Data     |
#                   ----------------------------------
#
#                        Figure 5-3: ACK packet
#
#                         2 bytes     2 bytes
#                         ---------------------
#                        | Opcode |   Block #  |
#                         ---------------------
#
#                        Figure 5-4: ERROR packet
#
#               2 bytes     2 bytes      string    1 byte
#               -----------------------------------------
#              | Opcode |  ErrorCode |   ErrMsg   |   0  |
#               -----------------------------------------
#
# To do:
#       - implement shell function.
#           * Welcome screen
#           * Shell commands:
#               1. Connect (IP, Port)
#               2. Read
#               3. Write
#               4. Exit
#               5. Help
#       - implement form packet methods for 5 packet types
#       - does the client form error packets?
import socket
import sys


class TFTPClient:
    def __init__(self, serverHost, serverPort):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.socket = None
        self.response = None
        self.encoding = 'utf-8'

    def socket_create(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
        # Ensures the data is in bytes (not string)
        try:
            payload = payload.encode()
        except AttributeError:
            pass

        try:
            self.socket.sendto(payload, (self.serverHost, self.serverPort))
        except socket.error as sockerr:
            print("Socket error: {}".format(sockerr))
        except IOError as ioerr:
            print("IO error: {}".format(ioerr))

    def form_rw_packet(self, filename, mode):
        pass

    def form_data_packet(self, blocknum, data):
        pass

    def receive_response(self):
        data, addr = self.socket.recvfrom(65535)
        return data, addr

    def socket_close(self):
        try:
            self.socket.close()
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()
