# hashes a raw file number (string type)
# handles exceptions
def hash(raw_file_no):
    # check valid input
    try:
        int(raw_file_no)
    except:
        return None
    
    file_no = int(raw_file_no)
    if file_no < 0 or file_no > 9999:
        return None

    return file_no % 256

# determines if a peer is responsible for owning a particular file
def has_file(own_id, requestor_id, successor_id, predecessor_id, hashed_file_no):
    # if peer id matches hashed file no
    if own_id == hashed_file_no:
        return True
    # if you are immediate successor
    elif own_id > hashed_file_no and predecessor_id < hashed_file_no:
        return True
    # if you are immediate successor but previous peer has a larger ID (start of loop)
    elif own_id < predecessor_id and predecessor_id < hashed_file_no:
        return True
    # otherwise, we are not responsible for the file
    else:
        return False

# writes to an open log
def write_to_log(open_log_file, event=None, time=None, seq=0, no_bytes=0, ack=0):
    open_log_file.write(f'{event}\t\t\t {time}\t\t\t {seq}\t\t\t {no_bytes}\t\t\t {ack}\n')





    



