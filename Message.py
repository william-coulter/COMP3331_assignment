# Message class for pickle usage

class message():
    def __init__(self, data=None, ack_no=None, seq_no=None, MSS=None):
        self._data = data
        self._ack_no= ack_no
        self._seq_no = seq_no
        self._MSS = MSS

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