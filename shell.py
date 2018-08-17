# Author: Nick Abbott       Date: 08-17-2018
# Shell class contains TFTPClient object and is the user
# interface to the TFTP Server.

from TFTPClient import *
import sys
import socket

class Shell:
    def __init__(self):
        self.client = None
        self.connection = socket.gethostname()
        self.commands = ['connect <ip> <port>', 'read <file> <mode>', 'write <file> <mode>', 'exit', 'help']

    def run(self):
        print("Courier is a TFTP software program written in python 3.6")
        print("Enter help for help menu")
        try:
            while True:
                cmd = input("{}>".format(self.connection))
                cmd = cmd.split() # Convert cmd from string to list
                if cmd[0] == 'connect':
                    self.connect(cmd)
                elif cmd[0] == 'read':
                    self.read(cmd)
                elif cmd[0] == 'write':
                    self.write(cmd)
                elif cmd[0] == 'exit':
                    self.exit()
                elif cmd[0] == 'help':
                    self.help()
                else:
                    print("Unknown command: {}".format(" ".join(cmd)))
        except KeyboardInterrupt as intr:
            return

    def connect(self, cmd):
        self.client = TFTPClient(cmd[1], int(cmd[2]))
        self.client.socket_create()
        self.client.socket_connect()
        self.connection = self.client.serverHost

    def read(self, cmd):
        request = '1{}0{}0'.format(cmd[1], cmd[2])
        self.client.request(request)
        data, addr = self.client.receive_response()
        print("Response from {}: {}".format(self.client.serverHost, str(data, 'utf-8')))


    def write(self, cmd):
        request = "2{}0{}0".format(cmd[1], cmd[2])
        self.client.request(request)
        data, addr = self.client.receive_response()
        print("Response from {}: {}".format(self.client.serverHost, str(data, 'utf-8')))

    def exit(self):
        if self.client is not None:
            self.client.socket_close()
        if self.connection != socket.gethostname():
            self.connection = socket.gethostname()
        else:
            sys.exit()

    def help(self):
        print("Commands: ")
        for cmd in self.commands:
            print("\t{}".format(cmd))



if __name__ == "__main__":
    shell = Shell()
    shell.run()
