#Encrypt messages with fernet
from cryptography.fernet import Fernet
import json
import os
from store import Store
import datetime
# import pprint
class Encryptor(object):
	def __init__(self):
		# self.fileName = fileName
		self.dbUser = os.environ['API_USER']
		self.dbPw = os.environ['API_PASSWORD']
		self.st = Store(self.dbUser,self.dbPw)
	def encrypt(self,message):
		key = Fernet.generate_key()
		f = Fernet(key)	
		encoded = message.encode()
		encrypted = f.encrypt(encoded)
		hsh = self.generate_hash(encrypted)
		_strkey = key.decode()
		doc = {
			"hsh":hsh,
			"key":_strkey,
			"destroy":False,
			"date":datetime.datetime.utcnow()
		}
		self.st.add(doc)
		return encrypted
	def decrypt(self,encryptedMessage,destroy = False):
		hsh = self.generate_hash(encryptedMessage)
		d = self.st.find({'hsh':hsh})
		key = d['key'].encode()
		f = Fernet(key)
		_msg = encryptedMessage
		res = f.decrypt(_msg).decode()
		return res
	def generate_hash(self,encrypted):
		return encrypted.decode()

# if __name__ == '__main__':
# 	enc = Encryptor('data.json')
# 	_encrypted = enc.encrypt('I am batman')
# 	enc.decrypt(_encrypted)
