import sys
import socket
import threading
import time
import pickle

from Messages import requestFileMessage

# requests file from successor
class fileRequest(threading.Thread):
    def __init__(self, id, successor, requestor_id, file_no):
        threading.Thread.__init__(self)
        self._id = id
        self._successor = successor
        self._requestor_id = requestor_id
        self._file_no = file_no
        
    def run(self):  
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:                  
            # create pickle message
            request = requestFileMessage(self._requestor_id, self._file_no, self._id)
            msg = pickle.dumps(request)
        
            # send request to successor
            s.connect(("127.0.0.1", 50000 + int(self._successor)))
            s.sendall(msg)       
            
            print('sending file request to successor')
            
            # wait for response from eventual responder
            # data = s.recv(1024) MAYBE????