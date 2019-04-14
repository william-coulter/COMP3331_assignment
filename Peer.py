
import sys
import socket
import threading
import time
import pickle

from Functions import hash
from errors import fileNoInputError, check_fileno_input
from Message import message

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
    
    # sends pings through UDP socket 
    def ping_successor(self, successor):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:     
        
            # ping sends id of sender
            msg = bytes(self._id, 'utf-8')
            s.sendto(msg, ("127.0.0.1", 50000 + int(successor))) 
            # this could be where deceased successors is handled
            # 
            #


            data, address = s.recvfrom(self._max_seg_size)
            print(f'A ping response message was received from Peer {successor}')

            s.close()

    # binds to a UDP socket that handles pings
    def handle_ping(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind(("127.0.0.1", 50000 + int(self._id)))
            
            pings_to_receive = 2
            while pings_to_receive > 0:
                data, addr = s.recvfrom(self._max_seg_size)
                data = data.decode('utf-8')

                print(f'A ping request message was received from Peer {data}')
                msg = bytes(self._id, 'utf-8')
                s.sendto(msg, addr)

                pings_to_receive -= 1

            s.close()

    def file_transfer_client(self, command, file_no=None):
        # just for testing
        # if (file_no == self._id):
        #input_string = input("").split()
        #command = input_string[0]
        #file_no = input_string[1]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            file_no = hash(file_no)
        
            # send request to successor
            s.connect(("127.0.0.1", 50000 + int(self._successor_1)))
            msg = bytes(f'{self._id} {file_no} {self._id}', 'utf-8')
            s.send(msg)

            print('sending file request to successor')
            
            # wait for response from responder
            data = s.recv(self._max_seg_size)

            s.close()
        


    def file_transfer_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
            s.bind(("127.0.0.1", 50000 + int(self._id)))
            # listen up to 5 requests in queue
            s.listen(5)

            conn, addr = s.accept()
            while True:             
                data = conn.recv(self._max_seg_size)
                if not data: break
            
                data = data.decode('utf-8')
                predecessor = data.split()[0]
                hashed_file_no = hash(data.split()[1])
                requestor = data.split()[2]

                if has_file(self._id, requestor, self._successor_1, predecessor, hashed_file_no):
                    print(f'I have file')
                else: 
                    s.connect(("127.0.0.1", 50000 + int(self._successor_1)))
                    msg = bytes(f'{self._id} {file_no} {self._id}', 'utf-8')
                    s.send(msg)
                


            conn.close()