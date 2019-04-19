import sys
import socket
import threading
import time
import pickle

from Messages import fileTransferMessage

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
            
            s.bind(("127.0.0.1", 50000 + self._id))

            with open(f'{self._file_no}' + '.pdf', 'rb') as f:
                bytes_read = f.read(self._MSS)
                ack_no = 0
                seq_no = 0

                while bytes_read:
                    print('reading file')
                    data = fileTransferMessage(self._file_no, bytes_read, ack_no, seq_no, self._MSS, self._drop_prob)
                    msg = pickle.dumps(data)
                    s.sendto(msg, ('127.0.0.1', 50000 + self._requestor_id))

                    # wait for ACK
                    timeout = time.time() + 1                   
                    data, addr = s.recvfrom(1024)
                    if time.time() > timeout:
                        continue
                    
                    received_ack = pickle.loads(data).ack_no                    
                    print(f'received ack #{received_ack}')
                    # save ACK no

                    ack_no += 1
                    seq_no += self._MSS
                    bytes_read = f.read(self._MSS)
