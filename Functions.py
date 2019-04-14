from errors import fileNoInputError, check_fileno_input


# hashes a raw file number (string type)
# handles exceptions
def hash(raw_file_no):
    try:
        check_fileno_input(raw_file_no)       
        return int(raw_file_no) % 256
    except fileNoInputError as error:
        print(error.errors)

# determines if a peer is responsible for owning
# a particular file
# peer_id and hashed_file_no are ints
def has_file(own_id, requestor_id, successor_id, predecessor_id=None, hashed_file_no):
    # initial request
    if predecessor == None:






    



