import fire
from encryptMessage import Encryptor

class Encrypto(object):
    """
        CLI encrypto object
    """
    def __init__(self):
        self.encryptor = Encryptor('data.json')
    def encrypt(self,msg):
        encrypted = self.encryptor.encrypt(msg)
        res = encrypted.decode()
        return res
    def decrypt(self,encrypted):
        inp = encrypted.encode()
        res = self.encryptor.decrypt(inp)
        return res

if __name__ == "__main__":
    fire.Fire(Encrypto)