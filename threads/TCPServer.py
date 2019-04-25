import socket
import threading
import time
import pickle

from threads.FileRequest import fileRequest
from threads.FileTransfer import fileTransfer
from threads.NewSuccessor import newSuccessor

from supporting.Messages import requestFileMessage, newSuccessorMessage, newPredecessorMessage, requestNewSuccessorMessage
from supporting.Functions import has_file

# handles requests over TCP
class TCPserver(threading.Thread):
    def __init__(self, id, successors, predecessors, MSS, drop_prob):
        threading.Thread.__init__(self)
        self._id = id
        self._successors = successors
        self._predecessors = predecessors
        self._MSS = MSS
        self._drop_prob = drop_prob
        
    def run(self):           
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
            s.bind(("127.0.0.1", 50000 + self._id))          
            s.listen(5) # listen up to 5 requests in queue

            # CHECK TYPE OF MESSAGE RECEIVED
            while True:             
                # depickle received message
                conn, addr = s.accept()
                data = conn.recv(1024)
                if not data: break
                
                received_msg = pickle.loads(data)

                # IF MESSAGE IS REQUESTING FILE
                if type(received_msg) is requestFileMessage:
                    
                    # test if we have the file
                    if has_file(self._id, received_msg.requestor_id, self._successors[0], received_msg.predecessor, received_msg.file_no):
                        # check if the request came initially from self
                        if self._id == received_msg.requestor_id: 
                            print('we have the file lmao')      # although according to spec this should not happen
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
                        fileRequestThread = fileRequest(self._id, self._successors[0], received_msg.requestor_id, received_msg.file_no)   
                        fileRequestThread.start()
                        fileRequestThread.join()

                # IF MESSAGE IS INFORMING US OF NEW SUCCESSORS
                elif type(received_msg) is newSuccessorMessage:
    
                    if self._successors[0] != received_msg.new_successors[0]:
                        self._successors[0] = received_msg.new_successors[0]
                        print(f'My first successor is now peer {self._successors[0]}.')
                    
                    if self._successors[1] != received_msg.new_successors[1]:
                        self._successors[1] = received_msg.new_successors[1]
                        print(f'My second successor is now peer {self._successors[1]}.')

                # IF MESSAGE IS INFORMING US OF NEW PREDECESSORS
                elif type(received_msg) is newPredecessorMessage:
                    print(f'first is: {received_msg.new_predecessors[0]}')
                    print(f'second is: {received_msg.new_predecessors[1]}')
                    self._predecessors[0] = received_msg.new_predecessors[0]
                    self._predecessors[1] = received_msg.new_predecessors[1]
                
                # IF MESSAGE IS ASKING FOR SENDER PEER'S SUCCESSORS        
                elif type(received_msg) is requestNewSuccessorMessage:
                    # establish if it was the requesting peer's immediate successor who died
                    if received_msg.is_immediate:
                        # this means their old 2nd successor is their new 1st successor
                        # and my 1st successor is their 2nd successor
                        newSuccessorThread = newSuccessor(received_msg.id, [received_msg.prev_successors[1], self._successors[0]])
                        newSuccessorThread.start()
                        newSuccessorThread.join()
                    else:
                        # This means my 1st successor should be their 2nd successor
                        # assuming both my successors are alive........
                        newSuccessorThread = newSuccessor(received_msg.id, [received_msg.prev_successors[0], self._successors[0]])
                        newSuccessorThread.start()
                        newSuccessorThread.join()
                
                conn.close()