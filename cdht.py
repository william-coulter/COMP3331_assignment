# COMP3331 Assignment
# Written by William Coulter z5113817
import sys
import threading
import time

from threads.TCPServer import TCPserver
from threads.UDPServer import UDPserver
from threads.PingRequest import pingRequest
from threads.FileRequest import fileRequest
from threads.NewSuccessor import newSuccessor
from threads.NewPredecessor import newPredecessor
from threads.Ping import ping

from supporting.Functions import hash, has_file

# add all inputs from cmd line
peer_id         = int(sys.argv[1])
successors      = [int(sys.argv[2]), int(sys.argv[3])]
predecessors    = ['2', 'elements']        
MSS             = int(sys.argv[4])
drop_prob       = float(sys.argv[5])

# run server for rest of execution
TCPServerThread = TCPserver(peer_id, successors, predecessors, MSS, drop_prob)
UDPServerThread = UDPserver(peer_id, successors, predecessors)
TCPServerThread.start()
UDPServerThread.start()
time.sleep(0.5)

# peers ping each other throughout execution to test if alive
pingThread = ping(peer_id, successors)
pingThread.start()
time.sleep(0.5)

# this is where cmd line input is handled
while True:
    initial_input = input()
    command = initial_input.split()[0]
    
    # if request input
    if command == "request":
        file_no = hash(initial_input.split()[1])
        if file_no == None:
            print('Please input a valid filename between 0000 and 9999')
            continue

        # send request to successor
        fileRequestThread = fileRequest(peer_id, successors[0], peer_id, file_no)   
        fileRequestThread.start()
        fileRequestThread.join()     

    # if peer departure input
    elif command == "quit":
        print(f'Peer {peer_id} will depart from the network')
        
        # send messages to assign new predecessors and successors
        newSuccessorImmediateThread = newSuccessor(predecessors[0], [successors[0], successors[1]])
        newSuccessorThread = newSuccessor(predecessors[1], [predecessors[0], successors[0]])
        newPredecessorImmediateThread = newPredecessor(successors[0], [predecessors[0], predecessors[1]])
        newPredecessorThread = newPredecessor(successors[1], [successors[0], predecessors[0]])
        
        newSuccessorImmediateThread.start()
        newSuccessorThread.start()
        newPredecessorImmediateThread.start()
        newPredecessorThread.start()
        
        newSuccessorImmediateThread.join()
        newSuccessorThread.join()
        newPredecessorImmediateThread.join()
        newPredecessorThread.join()
        time.sleep(0.2)

        # not sure how to exit terminal
        sys.exit()
    else:
        print('invalid input')
        continue     

pingThread.join()
TCPServerThread.join()
UDPServerThread.join()