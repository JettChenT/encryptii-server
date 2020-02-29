#Encrypt messages with AES 256
from cryptography.fernet import Fernet
import json
import pprint
class Encryptor(object):
	def __init__(self,fileName):
		self.fileName = fileName
	def encrypt(self,message):
		key = Fernet.generate_key()
		print("type:{}".format(type(key)))
		f = Fernet(key)	
		encoded = message.encode()
		encrypted = f.encrypt(encoded)
		print('lol')
		hsh = self.generate_hash(encrypted)
		print('yay')
		with open(self.fileName) as f:
			data = json.load(f)
		print(data)
		_strkey = key.decode()
		data[hsh] = {
			"key":_strkey
		}
		pprint.pprint(data)
		print('horay!')
		with open(self.fileName,'w') as f:
			json.dump(data,f)
		return encrypted
	def decrypt(self,encryptedMessage):
		with open(self.fileName) as f:
			data = json.load(f)
		hsh = self.generate_hash(encryptedMessage)
		key = data[hsh]["key"].encode()
		f = Fernet(key)
		_msg = encryptedMessage
		res = f.decrypt(_msg).decode()
		print(res)
		return res
	def generate_hash(self,encrypted):
		return encrypted.decode()

if __name__ == '__main__':
	enc = Encryptor('data.json')
	_encrypted = enc.encrypt('I am batman')
	enc.decrypt(_encrypted)
