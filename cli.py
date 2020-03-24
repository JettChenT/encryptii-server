import fire
from encryptMessage import Encryptor

class Encrypto(object):
    """
        CLI encrypto object
    """
    def __init__(self):
        self.encryptor = Encryptor()
    def encrypt(self,msg):
        encrypted = self.encryptor.encrypt(msg)
        res = encrypted.decode()
        return res
    def decrypt(self,encrypted,destroy = False):
        inp = encrypted.encode()
        res = self.encryptor.decrypt(inp,destroy = destroy)
        return res

if __name__ == "__main__":
    fire.Fire(Encrypto)