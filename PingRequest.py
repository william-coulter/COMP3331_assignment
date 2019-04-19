import sys
import socket
import threading
import time
import pickle

from Messages import pingMessage

# sends pings through UDP socket 
class pingRequest(threading.Thread):
    def __init__(self, id, successor):
        threading.Thread.__init__(self)
        self._id = id
        self._successor = successor
        
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:     

            # ping sends id of sender
            ping = pingMessage(self._id)
            msg = pickle.dumps(ping)
            s.sendto(msg, ("127.0.0.1", 50000 + int(self._successor))) 

            data, address = s.recvfrom(1024)
            received_msg = pickle.loads(data)
            print(f'A ping response message was received from Peer {received_msg.id}')

            s.close()