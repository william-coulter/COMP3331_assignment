# COMP3331 Assignment
# Written by William Coulter z5113817
import sys
import socket
import threading
import time
# import pickle

from PingRequest import pingRequest
from HandlePing import handlePing

# from Functions import hash
# from errors import fileNoInputError, check_fileno_input
# from Message import Message

# add all inputs from cmd line
peer_id = sys.argv[1]
successor_1 = sys.argv[2]
successor_2 = sys.argv[3]
MSS = int(sys.argv[4])
drop_prob = float(sys.argv[5])

# set-up separate threads for ping request
HandlePingThread = handlePing(peer_id)
PingRequestSucc1Thread = pingRequest(peer_id, successor_1)
PingRequestSucc2Thread = pingRequest(peer_id, successor_2)

# begin thread execution
HandlePingThread.start()
time.sleep(0.2)
PingRequestSucc1Thread.start()
PingRequestSucc2Thread.start()

# main thread waits until ping is completed
PingRequestSucc1Thread.join()
PingRequestSucc2Thread.join()
HandlePingThread.join()

# main thread continues here
print('all successors are alive')
'''
# Might need to loop this

file_transfer_server = threading.Thread(target=working_peer.file_transfer_server)
file_transfer_client = threading.Thread(target=working_peer.file_transfer_client)
file_transfer_server.start()
time.sleep(0.2) # wait for server to setup
file_transfer_client.start()

file_transfer_server.join()
file_transfer_client.join()

'''