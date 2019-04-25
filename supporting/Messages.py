# Message classes for pickle usage

# Send to confirm peers are alive
class pingMessage():
    def __init__(self, id, seq_no, is_immediate=False):
        self._id = id
        self._seq_no = seq_no
        self._is_immediate = is_immediate
        
    @property
    def id(self):
        return self._id
    
    @property
    def seq_no(self):
        return self._seq_no

    @property
    def is_immediate(self):
        return self._is_immediate

# Send to request file from successor
class requestFileMessage():
    def __init__(self, requestor_id, file_no, predecessor):
        self._requestor_id = int(requestor_id)
        self._file_no = int(file_no)
        self._predecessor = int(predecessor)
    
    @property
    def requestor_id(self):
        return self._requestor_id

    @property
    def file_no(self):
        return self._file_no

    @property
    def predecessor(self):
        return self._predecessor

# send once file has been located
class responseFileMessage():
    def __init__(self, id, file_no):
        self._id = id
        self._file_no = file_no
    
    @property
    def id(self):
        return self._id

    @property
    def file_no(self):
        return self._file_no

# send to transfer contents of file
class fileTransferMessage():
    def __init__(self, file_no=None, data=None, ack_no=None, seq_no=None, MSS=None, drop_prob=None):
        self._file_no = file_no
        self._data = data
        self._ack_no= ack_no
        self._seq_no = seq_no
        self._MSS = MSS
        self._drop_prob = drop_prob

    @property
    def file_no(self):
        return self._file_no

    @property
    def data(self):
        return self._data

    @property
    def ack_no(self):
        return self._ack_no

    @property
    def seq_no(self):
        return self._seq_no
    
    @property
    def MSS(self):
        return self._MSS

    @property
    def drop_prob(self):
        return self._drop_prob


class newSuccessorMessage():
    def __init__(self, new_successors):
        self._new_successors = new_successors

    @property
    def new_successors(self):
        return self._new_successors

class newPredecessorMessage():
    def __init__(self, new_predecessors):
        self._new_predecessors = new_predecessors

    @property
    def new_predecessors(self):
        return self._new_predecessors

class requestNewSuccessorMessage():
    def __init__(self, id, prev_successors, is_immediate):
        self._id = id
        self._prev_successors = prev_successors
        self._is_immediate = is_immediate

    @property
    def id(self):
        return self._id

    @property
    def prev_successors(self):
        return self._prev_successors

    @property
    def is_immediate(self):
        return self._is_immediate
