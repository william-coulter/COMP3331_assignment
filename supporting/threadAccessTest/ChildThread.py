import threading

class childThread(threading.Thread):
    def __init__(self, variablesToChange):
        threading.Thread.__init__(self)
        self._variablesToChange = variablesToChange

    def run(self):
        print(f'in child thread: before we change the variables {self._variablesToChange}')
        
        self._variablesToChange[0] = 'I '
        self._variablesToChange[1] = 'did it'
        