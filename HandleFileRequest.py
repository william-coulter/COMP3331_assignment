def file_transfer_server(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.bind(("127.0.0.1", 50000 + int(self._id)))
        # listen up to 5 requests in queue
        s.listen(5)

        conn, addr = s.accept()
        while True:             
            data = conn.recv(self._max_seg_size)
            if not data: break
        
            data = data.decode('utf-8')
            predecessor = data.split()[0]
            hashed_file_no = hash(data.split()[1])
            requestor = data.split()[2]

            if has_file(self._id, requestor, self._successor_1, predecessor, hashed_file_no):
                print(f'I have file')
            else: 
                s.connect(("127.0.0.1", 50000 + int(self._successor_1)))
                msg = bytes(f'{self._id} {file_no} {self._id}', 'utf-8')
                s.send(msg)
            
        conn.close()