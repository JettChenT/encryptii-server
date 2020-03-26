#Encrypt messages with fernet
from cryptography.fernet import Fernet
import json
import os
from store import Store
import datetime
import hashlib
# import pprint
class Encryptor(object):
	def __init__(self):
		# self.fileName = fileName
		self.dbUser = os.environ.get('API_USER')
		self.dbPw = os.environ.get('API_PASSWORD')
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
		if destroy:
			d = self.st.desFind({'hsh':hsh})
		else:
			d = self.st.find({'hsh':hsh})
		if d == {}:
			return -1
		key = d['key'].encode()
		f = Fernet(key)
		_msg = encryptedMessage
		res = f.decrypt(_msg).decode()
		return res
	def generate_hash(self,encrypted):
		return hashlib.sha224(encrypted).hexdigest()

# if __name__ == '__main__':
# 	enc = Encryptor('data.json')
# 	_encrypted = enc.encrypt('I am batman')
# 	enc.decrypt(_encrypted)
