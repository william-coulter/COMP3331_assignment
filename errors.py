from abc import ABC

class fileNoInputError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = ""
        super().__init__(msg)
        self._errors = errors

def check_fileno_input(file_no):
    errors = {}
    # test input is an int
    try:
        int(file_no)
    except:
        errors['not integer'] = "Please specify a file number of type integer"
    
    # test input is within valid range
    if int(file_no) < 0 or int(file_no) > 9999:
        errors['out of range'] = "Please specify a file number between 0 and 9999"
    
    # raise these errors
    if errors:
        raise fileNoInputError(errors)