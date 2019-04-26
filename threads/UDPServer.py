import sys
import socket
import threading
import time
import pickle

from supporting.Messages import pingMessage, fileTransferMessage, responseFileMessage
from supporting.Functions import write_to_log

# binds to a UDP socket that handles messages
class UDPserver(threading.Thread):
    def __init__(self, id, successors, predecessors):
        threading.Thread.__init__(self, daemon=True)
        self._id = id
        self._successors = successors
        self._predecessors = predecessors
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind(("127.0.0.1", 50000 + self._id))
            
            # CHECK TYPE OF MESSAGE RECEIVED
            while True:
                data, addr = s.recvfrom(1024)
                received_msg = pickle.loads(data)
                
                # IF PING MESSAGE WAS RECEIVED
                if type(received_msg) is pingMessage:
                    
                    print(f'A ping request message was received from Peer {received_msg.id}')
                    
                    # keep track of predecessor
                    if received_msg.is_immediate:
                        self._predecessors[0] = received_msg.id
                    else:
                        self._predecessors[1] = received_msg.id

                    # send ACK
                    ping = pingMessage(self._id, received_msg.seq_no)
                    msg = pickle.dumps(ping)
                    s.sendto(msg, addr)

                # IF MESSAGE WANTS TO CONFIRM WE CAN RECEIVE FILE
                elif type(received_msg) is responseFileMessage:
                    response_message = responseFileMessage(self._id, received_msg.file_no)
                    msg = pickle.dumps(response_message)
                    s.sendto(msg, addr)

                    print(f'Received a response message from peer {received_msg.id}, which has the file {received_msg.file_no}.')

                # IF MESSAGE WANTS US TO START ACCEPTING THE FILE 
                elif type(received_msg) is fileTransferMessage:
                    with open('requesting_log.txt', 'a') as requesting_log:

                        now = round(time.time(), 2)

                        if received_msg.seq_no == 1:
                            print('We now start receiving the file .........')

                        if received_msg.ack_no == 'final ack':
                            print('The file is received.')
                            continue
                        
                        # write to log that packet was received
                        event = 'rcv'
                        seq_no = received_msg.seq_no
                        no_bytes = sys.getsizeof(received_msg.data) 
                        ack_no = received_msg.ack_no
                        write_to_log(requesting_log, event, now, seq_no, no_bytes, ack_no)

                        # open file to store in
                        with open(f'new_{received_msg.file_no}' + '.pdf', 'ab') as received_file:
                            
                            # store in new file
                            received_file.write(received_msg.data)
                            
                            # send ACK                       
                            ack_no = received_msg.seq_no + no_bytes
                            ack = fileTransferMessage(ack_no=ack_no)
                            msg = pickle.dumps(ack)
                            s.sendto(msg, addr)
                            
                            # write to log that ack was sent
                            now = round(time.time(), 2)
                            event = 'snd'
                            write_to_log(requesting_log, event, now, 0, no_bytes, ack_no)