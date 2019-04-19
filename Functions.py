from errors import fileNoInputError, check_fileno_input

# hashes a raw file number (string type)
# handles exceptions
def hash(raw_file_no):
    try:
        check_fileno_input(raw_file_no)       
        return int(raw_file_no) % 256
    except fileNoInputError as error:
        return error

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




    



