import sys
import socket
import threading
import time
import pickle
import random

from Messages import pingMessage, fileTransferMessage, responseFileMessage

# binds to a UDP socket that handles pings
class UDPserver(threading.Thread):
    def __init__(self, id, drop_prob):
        threading.Thread.__init__(self)
        self._id = id
        self._drop_prob = drop_prob
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind(("127.0.0.1", 50000 + self._id))
            
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

                elif type(received_msg) is responseFileMessage:
                    response_message = responseFileMessage(self._id, received_msg.file_no)
                    msg = pickle.dumps(response_message)
                    s.sendto(msg, addr)
                    print(f'Received a response message from peer {received_msg.id}, which has the file {received_msg.file_no}.')

                elif type(received_msg) is fileTransferMessage:
                    with open('requesting_log.txt', 'a') as requesting_log:

                        # test if packet was lost
                        #if random.uniform(0, 1) < self._drop_prob:
                            #print('oops, lost this packet')
                            #continue
                        
                        now = round(time.time(), 2)

                        if received_msg.ack_no == 0:
                            print('We now start receiving the file .........')

                        if received_msg.ack_no == 'final ack':
                            print('The file is received.')
                            continue
                        
                        # write to log that packet was received
                        event = 'rcv'
                        seq_no = received_msg.seq_no
                        no_bytes = sys.getsizeof(received_msg.data) 
                        ack_no = received_msg.ack_no
                        requesting_log.write(f'{event}\t\t\t {now}\t\t\t {seq_no}\t\t\t {no_bytes}\t\t\t {ack_no}\n')

                        # open file to store in
                        with open(f'new_{received_msg.file_no}' + '.pdf', 'ab') as received_file:
                            
                            received_file.write(received_msg.data)
                            
                            # send ACK                       
                            ack_no = received_msg.seq_no + no_bytes
                            ack = fileTransferMessage(ack_no=ack_no)
                            msg = pickle.dumps(ack)
                            s.sendto(msg, addr)
                            
                            # write to log that ack was sent
                            now = round(time.time(), 2)
                            event = 'snd'
                            seq_no = 0
                            requesting_log.write(f'{event}\t\t\t {now}\t\t\t {seq_no}\t\t\t {no_bytes}\t\t\t {ack_no}\n')
