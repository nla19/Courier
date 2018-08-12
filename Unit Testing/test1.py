# Unit test: create program that pulls in (english) dictionary
#            and randomly assembles combinations of (> 5) words
#            to verify the server can identify a malformed packet.

import random
import sys

# Change filesystem path to directory containging TFTPClient.py
sys.path.insert(0, '..')
from TFTPClient import *

# List of english words
list = []
malformed = "Undetected Malformed Packets.txt"
malformed_counter = 0

# TFTP client
client = TFTPClient("192.168.1.8", 50008)
client.socket_create()

# Loop through file and store words in memory (specifically 'list')
with open("words.txt", 'rb') as words:
    for word in words:
        x = word.rstrip(b'\n')
        list.append(x)

    words.close()

with open(malformed, 'w') as out:
    for test in range(0, 1000):
        number_word = random.randrange(6)
        phrase = ''
        for word in range(0, number_word):
            response = client.request(phrase + str(list[random.randrange(446001)]) + ' ')
            if response != b'M':
                out.write(phrase)
                malformed_counter = malformed_counter + 1

    out.close()

client.socket_close()
