import random
import string
import hashlib

class stdlib():
    """
    Reusable library of custom functions
    """

    def __init__(self):
        super().__init__()


    # https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


    def makeRandomKey(self, length):
        letters = string.ascii_uppercase + string.digits
        return ( ''.join(random.choice(letters) for i in range(length)) )
