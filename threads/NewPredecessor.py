import socket
import threading
import pickle

from supporting.Messages import newPredecessorMessage

# sends information about new predecessor to target over TCP
class newPredecessor(threading.Thread):
    def __init__(self, target_id, new_predecessors):
        threading.Thread.__init__(self, daemon=True)
        self._target_id = target_id
        self._new_predecessors = new_predecessors
        
    def run(self):                   
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            information = newPredecessorMessage(self._new_predecessors)
            msg = pickle.dumps(information)
            s.connect(('127.0.0.1', 50000 + self._target_id))
            s.sendall(msg)

            
 
            

