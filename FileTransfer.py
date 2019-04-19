import sys
import socket
import threading
import time
import pickle
import signal
from contextlib import contextmanager

from Messages import fileTransferMessage, responseFileMessage

# sends from UDP socket to send file
class fileTransfer(threading.Thread):
    def __init__(self, id, requestor_id, file_no, MSS, drop_prob):
        threading.Thread.__init__(self)
        self._id = id
        self._requestor_id = requestor_id
        self._file_no = file_no
        self._MSS = MSS
        self._drop_prob = drop_prob 
        
    def run(self):                   
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            
            # s.settimeout(1)

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

                    while bytes_read:
                        data = fileTransferMessage(self._file_no, bytes_read, ack_no, seq_no, self._MSS, self._drop_prob)
                        msg = pickle.dumps(data)
                        s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))
                        
                        # write to log that packet was sent
                        event = 'snd'
                        now = round(time.time(), 2)
                        no_bytes = sys.getsizeof(bytes_read)
                        ack_no = 0
                        responding_log.write(f'{event}\t\t\t {now}\t\t\t {seq_no}\t\t\t {no_bytes}\t\t\t {ack_no}\n')

                        # wait for ACK
                        try:
                            data, addr = s.recvfrom(1024)
                        except TimeoutError: 
                            print('ack not received')
                            continue
                        
                        # write to log that ACK was received
                        event = 'rcv'
                        now = round(time.time(), 2)
                        seq_no = 0
                        no_bytes = sys.getsizeof(bytes_read)
                        ack_no = pickle.loads(data).ack_no                    
                        responding_log.write(f'{event}\t\t\t {now}\t\t\t {seq_no}\t\t\t {no_bytes}\t\t\t {ack_no}\n')

                        bytes_read = f.read(self._MSS)
                        seq_no = ack_no + sys.getsizeof(bytes_read)

                # once file has been sent, send end ACK
                final_ack = fileTransferMessage(ack_no='final ack')
                msg = pickle.dumps(final_ack)
                s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))
