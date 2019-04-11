# COMP3331 Assignment
# Written by William Coulter z5113817

import sys
import socket
import threading
import time


class peer():
    def __init__(self, id, successor_1, successor_2, max_seg_size, drop_prob):
        self._id = id
        self._successor_1 = successor_1
        self._successor_2 = successor_2
        self._max_seg_size = max_seg_size
        self._drop_prob = drop_prob

    def __str__(self):
        return f'Peer no. {self._id} with successors {self._successor_1} and {self._successor_2}.\n'

   
    @property
    def get_id(self):
        return self._id
   
    @property
    def get_successor_1(self):
        return self._successor_1

    @property
    def get_successor_2(self):
        return self._successor_2
    
    @property
    def get_max_seg_size(self):
        return self._max_seg_size

    @get_successor_1.setter
    def get_successor_1(self, new_successor_1):
        self._successor_1 = new_successor_1 

    @get_successor_2.setter
    def get_successor_2(self, new_successor_2):
        self._successor_2 = new_successor_2   
    
    
    # pings successors
    def ping_request(self):
                
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        time.sleep(1)

        # ping sends id of sender
        msg = bytes(self._id)
        
        client_sock.sendto(msg, ("127.0.0.1", 50000 + self._successor_1))
        client_sock.sendto(msg, ("127.0.0.1", 50000 + self._successor_2))      
        
        '''
        suc_1_is_alive = False
        suc_2_is_alive = False
        
        while suc_1_is_alive is False or suc_2_is_alive is False:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # ping sends id of sender
            msg = bytes(self._id)
            
            if suc_1_is_alive is False:
                client_sock.sendto(msg, ("127.0.0.1", 50000 + self._successor_1))
                # print (f'sending ping1 to peer{self._successor_1}\n')
            if suc_2_is_alive is False:
                client_sock.sendto(msg, ("127.0.0.1", 50000 + self._successor_2))
                # print (f'sending ping2 to peer{self._successor_2}\n')
            
            # wait for response            
            try:
                data, server = client_sock.recvfrom(self._max_seg_size)            
                # print(f'data received was {data}, from server {server}\n')
                
                if data == bytes(self.successor_1):
                    suc_1_is_alive = True
                if data == bytes(self.successor_2):
                    suc_2_is_alive = True

            except:
                print("something went wrong")
                exit(1)
        '''

    # handle ping requests
    def ping_response(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        address = ("127.0.0.1", 50000 + self._id)
        server_sock.bind(address)
        
        pings_to_receive = 2
        while pings_to_receive > 0:
            data, address = server_sock.recvfrom(self._max_seg_size)
            print(f'A ping request message was received from Peer {data}')
            # send back id of predessessor
            # server_sock.sendto(data, address)
            pings_to_receive -= 1

# create working peer from cmd line input
working_peer = peer(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]))

# set-up separate threads for client and server
server_thread = threading.Thread(name="server_thread", target=working_peer.ping_response)
client_thread = threading.Thread(name="client_thread", target=working_peer.ping_request)

# begin thread execution
server_thread.start()
client_thread.start()

# main thread waits until server and client are done executing
client_thread.join()
server_thread.join()

