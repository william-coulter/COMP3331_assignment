# COMP3331 Assignment
# Written by William Coulter z5113817
import sys
import socket
import threading
import time
import pickle

from PingRequest import pingRequest
from Functions import hash
from errors import fileNoInputError, check_fileno_input
from Message import Message

# create working peer from cmd line input
working_peer = peer(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]))

# set-up separate threads for ping request
handle_ping = threading.Thread(target=working_peer.handle_ping)
ping_succ_1 = threading.Thread(target=working_peer.ping_successor, args=(working_peer.get_successor_1))
ping_succ_2 = threading.Thread(target=working_peer.ping_successor, args=(working_peer.get_successor_2))

# begin thread execution
handle_ping.start()
time.sleep(0.2)
ping_succ_1.start()
ping_succ_2.start()

# main thread waits until ping is completed
ping_succ_1.join()
ping_succ_2.join()
handle_ping.join()

# main thread continues here
print('all successors are alive')

# Might need to loop this

file_transfer_server = threading.Thread(target=working_peer.file_transfer_server)
file_transfer_client = threading.Thread(target=working_peer.file_transfer_client)
file_transfer_server.start()
time.sleep(0.2) # wait for server to setup
file_transfer_client.start()

file_transfer_server.join()
file_transfer_client.join()

