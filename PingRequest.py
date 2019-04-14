import sys
import socket
import threading
import time
import pickle

# sends pings through UDP socket 
class pingRequest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
        
    def run(self):
        pass

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:     

            # ping sends id of sender
            msg = bytes(self._id, 'utf-8')
            s.sendto(msg, ("127.0.0.1", 50000 + int(successor))) 

            data, address = s.recvfrom(self._max_seg_size)
            print(f'A ping response message was received from Peer {successor}')

            s.close()