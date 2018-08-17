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
                filename, mode = self.decode_rw_packet(payload)
                response = "Read request from {}\nFilename: {} | Mode: {}".format(self.clientaddr[0], filename, mode)
                print(response)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '2':
                filename, mode = self.decode_rw_packet(payload)
                response = "Write request from {}\nFilename: {} | Mode: {}".format(self.clientaddr[0], filename, mode)
                print(response)
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '3':
                blocknum, data = self.decode_data_packet(payload)
                response = "Data from {}".format(self.clientaddr[0])
                print(response)
                print("Block number: {}, Data: {}".format(blocknum, data))
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '4':
                response = "Acknowledge from {}".format(self.clientaddr[0])
                acknum = self.decode_ack_packet(payload)
                print(response)
                print("Acknowledgement Number: {}".format(acknum))
                self.socket.sendto(bytes(response, 'utf-8'), self.clientaddr)
            elif chr(payload[0]) == '5':
                response = "Error from {}".format(self.clientaddr[0])
                error_code, error_msg = self.decode_error_packet(payload)
                print(response)
                print("Error code: {}, Error msg: {}".format(error_code, error_msg))
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
        except KeyboardInterrupt as intr:
            self.socket_close()
            sys.exit()

    def socket_close(self):
        try:
            self.socket.close()
        except socket.error as err:
            print("Socket error: {}".format(err))
            sys.exit()

    def decode_rw_packet(self, payload):
        filename = payload[1:str(payload).find('0') - 2]
        mode = payload[str(payload).find('0') -1:str(payload).rfind('0') - 2]
        return filename, mode

    def decode_data_packet(self, payload):
        print(payload)
        blocknum = payload[2:4]
        data = payload[5:]
        return blocknum, data

    def decode_ack_packet(self, payload):
        print(payload)
        ack = payload[2:]
        return ack

    def decode_error_packet(self, payload):
        print(payload)
        error_code = payload[2:4]
        error_msg = payload[5:-1]
        return error_code, error_msg


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
