import socket
import threading
import pickle

from supporting.Messages import newSuccessorMessage

# sends information about new successor to target over TCP
class newSuccessor(threading.Thread):
    def __init__(self, target_id, new_successors):
        threading.Thread.__init__(self, daemon=True)
        self._target_id = target_id
        self._new_successors = new_successors
        
    def run(self):                   
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            information = newSuccessorMessage(self._new_successors)
            msg = pickle.dumps(information)
            s.connect(('127.0.0.1', 50000 + self._target_id))
            s.sendall(msg)

            
 
            

