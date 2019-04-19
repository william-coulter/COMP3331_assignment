import sys
import socket
import threading
import time
import pickle

from Messages import pingMessage
from Messages import fileTransferMessage

# binds to a UDP socket that handles pings
class UDPserver(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self._id = id
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind(("127.0.0.1", 50000 + int(self._id)))
            
            while True:
                data, addr = s.recvfrom(1024)
                received_msg = pickle.loads(data)
                
                # check if ping was received
                if type(received_msg) is pingMessage:
                    print(f'A ping request message was received from Peer {received_msg.id}')
                    
                    # send ACK
                    ping = pingMessage(self._id)
                    msg = pickle.dumps(ping)
                    s.sendto(msg, addr)

                elif type(received_msg) is fileTransferMessage:
                    # if random_gen_no < drop_prob, continue
                    # open file to store in
                    with open(f'new_{received_msg.file_no}' + '.pdf', 'ab') as f:
                        
                        f.write(received_msg.data)
                        print(f'{received_msg.ack_no} {received_msg.seq_no}')
                        
                        # send ACK
                        ack = fileTransferMessage(ack_no=received_msg.ack_no)
                        msg = pickle.dumps(ack)
                        s.sendto(ack, addr)