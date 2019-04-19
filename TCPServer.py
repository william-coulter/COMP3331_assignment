import sys
import socket
import threading
import time
import pickle

from FileRequest import fileRequest
from FileTransfer import fileTransfer

from Messages import requestFileMessage
from Functions import has_file

# handles a file request
class TCPserver(threading.Thread):
    def __init__(self, id, successor, MSS, drop_prob):
        threading.Thread.__init__(self)
        self._id = id
        self._successor = successor
        self._MSS = MSS
        self._drop_prob = drop_prob
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
            s.bind(("127.0.0.1", 50000 + self._id))
            # listen up to 5 requests in queue
            s.listen(5)

            while True:             
                # depickle received message
                conn, addr = s.accept()
                data = conn.recv(1024)
                if not data: break
                received_msg = pickle.loads(data)

                # determine what to do with data
                if type(received_msg) is requestFileMessage:
                    
                    # test if we have the file
                    if has_file(self._id, received_msg.requestor_id, self._successor, received_msg.predecessor, received_msg.file_no):
                        # check if the request came initially from self
                        if self._id == received_msg.requestor_id: 
                            print('we have the file lmao')
                            continue
                        
                        # if not, send file to requestor
                        fileTransferThread = fileTransfer(self._id, received_msg.requestor_id, received_msg.file_no, self._MSS, self._drop_prob)
                        print(f'File {received_msg.file_no} is here.')
                        fileTransferThread.start()
                        fileTransferThread.join()
                        print('The file is sent.')
                    
                    # ask successor for file
                    else:
                        print(f'File {received_msg.file_no} is not stored here.')
                        fileRequestThread = fileRequest(self._id, self._successor, received_msg.requestor_id, received_msg.file_no)   
                        fileRequestThread.start()
                        fileRequestThread.join()     

                conn.close()