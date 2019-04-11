# python program for COMP3331 Lab02
# written by William Coulter on 10/03/2019
# version 3.7.2
#  
# sends 10 pings to server 1 second apart. 
# each ping contains:
#   - keyword PING
#   - sequence number
#   - timestamp
#
# should use host IP 127.0.0.1 

import os
import sys
import socket
import time

# receive host and port from command-line
host = sys.argv[1]
port = int(sys.argv[2])

# create socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:
    # set time out value at 1 second
    socket.settimeout(1.0)
    
    # begin sending pings
    for i in range(10):
                  
        # get time ping was sent
        start = time.time()        

        # send ping
        msg = bytes(f'PING {i} {start}\r\n', 'utf-8')
        socket.sendto(msg, (host, port))
        
        # assuming no timeout occurs
        try:
            # wait for response
            socket.recvfrom(1024)
            end = time.time()

            # print result
            rtt = (end - start) * 1000
            print(f'ping to {host}, seq = {i}, rtt = {rtt} ms')
        
        # if timeout happens    
        except:
            print(f'ping to {host}, seq = {i}, rtt = TIME-OUT')
        
        # wait before sending another message
        time.sleep(1)

