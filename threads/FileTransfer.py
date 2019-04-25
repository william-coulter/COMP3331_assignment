import sys
import socket
import threading
import time
import pickle
import random

from supporting.Messages import fileTransferMessage, responseFileMessage
from supporting.Functions import write_to_log

# transfers file over UDP
class fileTransfer(threading.Thread):
    def __init__(self, id, requestor_id, file_no, MSS, drop_prob):
        threading.Thread.__init__(self, daemon=True)
        self._id = id
        self._requestor_id = requestor_id
        self._file_no = file_no
        self._MSS = MSS
        self._drop_prob = drop_prob 
        
    def run(self):                   
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            with open('responding_log.txt', 'a') as responding_log:
                
                # send response message to requesting peer
                response_message = responseFileMessage(self._id, self._file_no)
                msg = pickle.dumps(response_message)
                s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))

                print(f'A response message, destined for peer {self._requestor_id}, has been sent.')
                data, addr = s.recvfrom(1024)
                received_msg = pickle.loads(data)
                if type(received_msg) is not responseFileMessage:
                    print('received incorrect ACK from requestor peer')
                    return

                # start sending file
                print('We now start sending the file .........')

                with open(f'{self._file_no}' + '.pdf', 'rb') as f:
                    
                    bytes_read = f.read(self._MSS)
                    seq_no = 1
                    ack_no = 0
                    RTX = False         # flag for retransmission  
                    while bytes_read:
                        
                        # test if packet was lost
                        if random.uniform(0, 1) < self._drop_prob:
                            # write to log that packet was lost
                            now = round(time.time(), 2)
                            event = 'Drop'
                            if RTX == True:
                                event += '/RTX'                                
                            no_bytes = sys.getsizeof(bytes_read)
                            write_to_log(responding_log, event, now, seq_no, no_bytes, 0)
                            RTX = True

                            time.sleep(1)       # simulate timeout
                            continue

                        data = fileTransferMessage(self._file_no, bytes_read, ack_no, seq_no, self._MSS, self._drop_prob)
                        msg = pickle.dumps(data)
                        s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))
                        
                        # write to log that packet was sent
                        if RTX == True:
                            event = 'RTX'
                            RTX = False
                        else:
                            event = 'snd'
                        now = round(time.time(), 2)
                        no_bytes = sys.getsizeof(bytes_read)
                        write_to_log(responding_log, event, now, seq_no, no_bytes, 0)
                                                    
                        # write to log that ACK was received
                        data, addr = s.recvfrom(1024)
                        event = 'rcv'
                        now = round(time.time(), 2)
                        no_bytes = sys.getsizeof(bytes_read)
                        ack_no = pickle.loads(data).ack_no                    
                        write_to_log(responding_log, event, now, 0, no_bytes, ack_no)
                        
                        # read next segment from file
                        bytes_read = f.read(self._MSS)
                        seq_no += sys.getsizeof(bytes_read)

                # once file has been sent, send end ACK
                final_ack = fileTransferMessage(ack_no='final ack')
                msg = pickle.dumps(final_ack)
                s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))
