# just for testing
    # if (file_no == self._id):
    #input_string = input("").split()
    #command = input_string[0]
    #file_no = input_string[1]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        file_no = hash(file_no)
    
        # send request to successor
        s.connect(("127.0.0.1", 50000 + int(self._successor_1)))
        msg = bytes(f'{self._id} {file_no} {self._id}', 'utf-8')
        s.send(msg)

        print('sending file request to successor')
        
        # wait for response from responder
        data = s.recv(self._max_seg_size)

        s.close()