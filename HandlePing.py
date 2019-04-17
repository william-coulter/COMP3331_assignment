import sys
import socket
import threading
import time

# binds to a UDP socket that handles pings
class handlePing(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self._id = id
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind(("127.0.0.1", 50000 + int(self._id)))
            
            pings_to_receive = 2
            while pings_to_receive > 0:
                data, addr = s.recvfrom(1024)
                data = data.decode('utf-8')

                print(f'A ping request message was received from Peer {data}')
                msg = bytes(self._id, 'utf-8')
                s.sendto(msg, addr)

                pings_to_receive -= 1

            s.close()