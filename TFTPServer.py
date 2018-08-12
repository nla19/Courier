#   Author: Nick Abbott     Date: 08-11-18
#   Description: This file is my python 3 implementation of a TFTP server.
#                My motivation for this project was to better understand TFTP
#                and practice my programming skills.

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
# To do: decode methods for 5 packet types

import random
import socket
import sys


class TFTPServer:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.socket = None
        self.clientaddr = None # Tuple = (IP Address, Port)
        self.tid = random.randrange(65536) # random number 0 - 65535 inclusive

    def socket_create(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            sys.exit(1)

    def socket_bind(self):
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()

    def handle_request(self):
        try:
            payload, self.clientaddr = self.socket.recvfrom(65535)
            if chr(payload[0])== '1':
                response = "Read request from {}".format(self.clientaddr[0])
                print(response)
                filename, mode = self.decode_read_packet(payload)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '2':
                response = "Write request from {}".format(self.clientaddr[0])
                print(response)
                filename, mode = self.decode_write_packet(payload)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '3':
                respone = "Data from {}".format(self.clientaddr[0])
                print(response)
                blocknum, data = self.decode_data_packet(payload)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '4':
                response = "Acknowledge from {}".format(self.clientaddr[0])
                print(response)
                acknum = self.decode_ack_packet(payload)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '5':
                response = "Error from {}".format(self.clientaddr[0])
                print(response)
                errcode, errmsg = self.decode_error_packet(payload)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            else:
                response = "Malformed packet from {}".format(self.clientaddr[0])
                print(response) #perhaps log
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
                print(payload)
            # print("handle_requestd {} bytes from {}: {}".format(len(payload), self.clientaddr[0], payload))
            return payload
        except socket.error as se:
            self.socket.sendto(b'Socket error raised', self.clientaddr)

    def socket_close(self):
        try:
            self.socket.close()
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()

    def decode_read_packet(self, payload):
        print(payload)
        return None, None


    def decode_write_packet(self, payload):
        print(payload)
        return None, None


    def decode_data_packet(self, payload):
        print(payload)
        return None, None

    def decode_ack_packet(self, payload):
        print(payload)
        return None

    def decode_error_packet(self, payload):
        print(payload)
        return None, None


if __name__ == "__main__":
    server = TFTPServer(50008)
    server.socket_create()
    server.socket_bind()
    try:
        while True:
            data = server.handle_request()
    except KeyboardInterrupt as intr:
        pass
    server.socket_close()
