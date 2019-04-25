import threading
import time

from threads.PingRequest import pingRequest

# constantly runs threads to ping successors
class ping(threading.Thread):
    def __init__(self, peer_id, successors):
        threading.Thread.__init__(self, daemon=True)
        self._peer_id = peer_id
        self._successors = successors
        
    def run(self):
        ping_seq_no = 0
        most_recent_seq_no_immediate = [ping_seq_no]
        most_recent_seq_no_not_immediate = [ping_seq_no]
        while True:
            # ping successors
            PingRequestSucc1Thread = pingRequest(self._peer_id, self._successors, ping_seq_no, most_recent_seq_no_immediate, is_immediate=True)
            PingRequestSucc2Thread = pingRequest(self._peer_id, self._successors, ping_seq_no, most_recent_seq_no_not_immediate)
            PingRequestSucc1Thread.start()
            PingRequestSucc2Thread.start()
            PingRequestSucc1Thread.join()
            PingRequestSucc2Thread.join()
            
            ping_seq_no += 1
            time.sleep(2)






