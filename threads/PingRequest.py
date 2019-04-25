import socket
import threading
import time
import pickle

from threads.RequestNewSuccessor import requestNewSuccessor
from threads.NewPredecessor import newPredecessor

from supporting.Messages import pingMessage

# sends ping to successor over UDP. Handles peer death
class pingRequest(threading.Thread):
    def __init__(self, id, successors, seq_no, most_recent_seq_no, is_immediate=False):
        threading.Thread.__init__(self, daemon=True)
        self._id = id
        self._successors = successors
        # self._predecessors = predecessors
        self._seq_no = seq_no
        self._most_recent_seq_no = most_recent_seq_no
        self._is_immediate = is_immediate
        
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:     
            s.settimeout(1)

            # send ping to successor
            ping = pingMessage(self._id, self._seq_no, self._is_immediate)
            msg = pickle.dumps(ping)
            if self._is_immediate:
                successor_to_send = self._successors[0]
            else:
                successor_to_send = self._successors[1]

            s.sendto(msg, ("127.0.0.1", 50000 + successor_to_send)) 

######################### PEER DEATH IS HANDLED BELOW #########################
            
            # wait for response and update most recent seq number received
            try:
                data, address = s.recvfrom(1024)
                received_msg = pickle.loads(data)
                if received_msg.seq_no == 0:
                    print(f'A ping response message was received from Peer {received_msg.id}')
                self._most_recent_seq_no[0] = received_msg.seq_no
            
            # if timeout occurs, check if this is the 4th time
            except:
                if self._seq_no - self._most_recent_seq_no[0] > 3:
                    print(f'Peer {successor_to_send} is no longer alive.')
                    
                    # ask over TCP who new successor is
                    requestNewSuccessorThread = requestNewSuccessor(self._id, self._successors, self._is_immediate)
                    requestNewSuccessorThread.start()
                    requestNewSuccessorThread.join()

                    # reset most_recent_seq_no
                    self._most_recent_seq_no[0] = 0