from cryptography.fernet import Fernet
import json
import os
from store import Store
import datetime
import hashlib
from emoji import EmojiConverter
import zlib


def generate_hash(encrypted) -> str:
    # generate sha256 hash for text
    return hashlib.sha256(encrypted).hexdigest()


class Encryptor(object):
    """
        The Encryptor object, handles encryption and decryption
    """

    def __init__(self):
        # process mongodb environs
        try:
            self.dbUser = os.environ.get("API_USER")
            self.dbPw = os.environ.get("API_PASSWORD")
        except:
            self.dbUser = 0
            self.dbPw = 0
        self.dbUrl = os.environ.get("API_URL")
        # Add store object to interact with the database
        self.st = Store(self.dbUrl, self.dbUser, self.dbPw)
        # Emoji converter
        self.conv = EmojiConverter("emojList.txt")

    def encrypt(self, message, emoji=False)->str:
        # Use fernet to generate key
        key = Fernet.generate_key()
        f = Fernet(key)
        # Compress the intended message via zlib
        encoded = zlib.compress(message.encode())
        # The encryption
        encrypted = f.encrypt(encoded)
        # Generate the hash of the encrypteds tring
        hsh = generate_hash(encrypted)
        # decoded key to store in mongodb
        _strkey = key.decode()
        # Store data in mongodb
        doc = {
            "hsh": hsh,
            "key": _strkey,
            "destroy": False,
            "compress": "zlib",
            "date": datetime.datetime.utcnow(),
        }
        self.st.add(doc)
        # Return the encrypted message
        encrypted = encrypted.decode()
        if emoji:
            encrypted = self.conv.sentence_to_emoji(encrypted)
        return encrypted

    def decrypt(self, encryptedMessage, destroy=False)->str:
        # hashing the message
        em = encryptedMessage.decode()
        if self.conv.is_emoji(em[0]):
            encryptedMessage = self.conv.emoji_to_sentence(em).encode()
        hsh = generate_hash(encryptedMessage)
        # Find the dataset in mongodb
        if destroy:
            d = self.st.desFind({"hsh": hsh})
        else:
            d = self.st.find({"hsh": hsh})
        if d == None:
            return -1
        # decrypt with key
        key = d["key"].encode()
        f = Fernet(key)
        _msg = encryptedMessage
        res = f.decrypt(_msg)
        res = zlib.decompress(res).decode()
        return res

    def destroy(self, encryptedMessage) -> bool:
        hsh = generate_hash(encryptedMessage)
        fnd = self.st.desFind({"hsh": hsh})
        return fnd != {}
