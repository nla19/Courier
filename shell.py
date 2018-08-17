from TFTPClient import *

class Shell:
    def __init__(self, client):
        if isinstance(client, TFTPClient):
            self.client = client
        else:
            raise TypeError("Client must be of type: TFTPClient")

    def run(self):
        print("Courier is a TFTP software program written in python 3.6")
        print("Enter help for help menu")
        try:
            while True:
                request = input("{}>".format(self.client.serverHost))
                self.client.request(request)
                data, addr = client.receive_response()
                print("Response from {}: {}".format(self.client.serverHost, str(data, "utf-8")))
        except KeyboardInterrupt as intr:
            return


if __name__ == "__main__":
    client = TFTPClient("192.168.1.9", 50008)
    shell = Shell(client)
    client.socket_create()
    shell.run()
    client.socket_close()
