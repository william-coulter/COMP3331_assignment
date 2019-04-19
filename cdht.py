# COMP3331 Assignment
# Written by William Coulter z5113817
import sys
import socket
import threading
import time

from TCPServer import TCPserver
from UDPServer import UDPserver
from PingRequest import pingRequest
from FileRequest import fileRequest

from Functions import hash, has_file


# add all inputs from cmd line
peer_id         = int(sys.argv[1])
successor_1     = int(sys.argv[2])
successor_2     = int(sys.argv[3])
MSS             = int(sys.argv[4])
drop_prob       = float(sys.argv[5])

# run server for rest of execution
TCPServerThread = TCPserver(peer_id, successor_1, MSS, drop_prob)
UDPServerThread = UDPserver(peer_id)
TCPServerThread.start()
UDPServerThread.start()
time.sleep(0.5)

# PUT THIS INTO A THREAD THAT CONSTANTLY CHECK STATUS OF PEERS  
# ping successors
PingRequestSucc1Thread = pingRequest(peer_id, successor_1)
PingRequestSucc2Thread = pingRequest(peer_id, successor_2)
PingRequestSucc1Thread.start()
PingRequestSucc2Thread.start()
PingRequestSucc1Thread.join()
PingRequestSucc2Thread.join()

while True:
    
    initial_input = input()
    command = initial_input.split()[0]
    if command == "request":
        file_no = hash(initial_input.split()[1])
        if has_file(peer_id, peer_id, successor_1, peer_id, file_no):
            # check if we have file
            print('we have it lmao')
            pass
        else :
            fileRequestThread = fileRequest(peer_id, successor_1, peer_id, file_no)   
            fileRequestThread.start()
            fileRequestThread.join()     

    elif command == "break":
        print('exiting loop')
        break
    else:
        print('invalid input')
        continue     

TCPServerThread.join()
UDPServerThread.join()