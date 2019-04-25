import socket
import threading
import pickle

from supporting.Messages import requestNewSuccessorMessage

# sends a message requesting for a new successor over TCP
class requestNewSuccessor(threading.Thread):
    def __init__(self, id, prev_successors, is_immediate=False):
        threading.Thread.__init__(self)
        self._id = id
        self._prev_successors = prev_successors
        self._is_immediate = is_immediate
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # send request for new successor to successor that is still alive
            request = requestNewSuccessorMessage(self._id, self._prev_successors, self._is_immediate)
            msg = pickle.dumps(request)

            # determine who to send request to
            if self._is_immediate:
                # this means the immediate successor was unresponsive
                successor_to_send = self._prev_successors[1]
            else:
                successor_to_send = self._prev_successors[0]
            
            s.connect(("127.0.0.1", 50000 + successor_to_send))
            s.sendall(msg)
