# Encrypt messages with fernet
from cryptography.fernet import Fernet
import json
import os
from store import Store
import datetime
import hashlib
from emoji import EmojiConverter


# import pprint
class Encryptor(object):
    def __init__(self):
        # self.fileName = fileName
        try:
            self.dbUser = os.environ.get("API_USER")
            self.dbPw = os.environ.get("API_PASSWORD")
        except:
            self.dbUser = None
            self.dbPw = None
        self.dbUrl = os.environ.get("API_URL")
        self.st = Store(self.dbUrl, self.dbUser, self.dbPw)
        self.conv = EmojiConverter("emojList.txt")

    def encrypt(self, message, emoji=False):
        key = Fernet.generate_key()
        f = Fernet(key)
        encoded = message.encode()
        encrypted = f.encrypt(encoded)
        hsh = self.generate_hash(encrypted)
        _strkey = key.decode()
        doc = {
            "hsh": hsh,
            "key": _strkey,
            "destroy": False,
            "date": datetime.datetime.utcnow(),
        }
        self.st.add(doc)
        encrypted = encrypted.decode()
        if emoji:
            encrypted = self.conv.sentence_to_emoji(encrypted)
        return encrypted

    def decrypt(self, encryptedMessage, destroy=False):
        em = encryptedMessage.decode()
        if self.conv.is_emoji(em[0]):
            encryptedMessage = self.conv.emoji_to_sentence(em).encode()
        hsh = self.generate_hash(encryptedMessage)
        if destroy:
            d = self.st.desFind({"hsh": hsh})
        else:
            d = self.st.find({"hsh": hsh})
        if d == None:
            return -1
        key = d["key"].encode()
        f = Fernet(key)
        _msg = encryptedMessage
        res = f.decrypt(_msg).decode()
        return res

    def destroy(self, encryptedMessage):
        hsh = self.generate_hash(encryptedMessage)
        fnd = self.st.desFind({"hsh": hsh})
        return fnd != {}

    def generate_hash(self, encrypted):
        return hashlib.sha224(encrypted).hexdigest()


# if __name__ == '__main__':
# 	enc = Encryptor('data.json')
# 	_encrypted = enc.encrypt('I am batman')
# 	enc.decrypt(_encrypted)
