#!/Users/muneebahmad/anaconda/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Beenum'

from Crypto import Random
from Crypto.Cipher import AES
import os
import sys
import base64
import binascii

class ED(object):
	def __init__(self, key, msg, bL=None):
		self.key = key
		self.msg = msg
		self.bL = bL

	def encrypt(self):
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		pad = lambda s: s + ((self.bL - len(s) % self.bL) * '{')
		#print base64.b64encode(iv)
		eMsg = base64.b64encode(iv + cipher.encrypt(pad(self.msg)))
		return eMsg

	def decrypt(self):
		
		iv = self.msg[:AES.block_size]
		print base64.b64encode(iv)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		dMsg = cipher.decrypt(self.msg[AES.block_size:]).rstrip('{')
		#print dMsg
		return dMsg

class runTest(object):
	def __init__(self, argv):
		usage = (
			'python %prog')
		bL = 32
		while True:
			mode = raw_input("Enter 'E' for encryption and 'D' for decryption: ")
			if mode == 'E':
				if os.path.exists("eTarget.txt") is True:
					with open('eTarget.txt', 'r') as myfile:
						msg = myfile.read()
				else:
					msg = raw_input("Enter the message you want to encrypt: ")
				#key = raw_input("Enter the key (optional): ")
				#print key
				#if key == '':
				key = os.urandom(bL)
				#key = Random.new().read(AES.block_size)
				print "Encryption key: %s" % base64.b64encode(key)
				a = ED(key, msg, bL)
				eMsg = a.encrypt()
				print "Encrypted Message: %s" % (eMsg)
				#print eMsg
				k = open('k.txt', 'w')
				k.write(base64.b64encode(key) + '\n')
				t = open('dTarget.txt', 'w')
				t.write(eMsg)
				break
			elif mode == 'D':
				if os.path.exists("dTarget.txt") is True:
					with open('dTarget.txt', 'r') as myfile:
						msg = myfile.read()
				else:
					msg = raw_input("Enter the message you want to encrypt: ")
					
				if os.path.exists("k.txt") is True:
					key = list(open('k.txt', 'r'))[0].strip('\n')
				else:
					key = raw_input("Enter the key (optional): ")
				print "Encryption key given is: %s" % key
				a = ED(base64.b64decode(key), base64.b64decode(msg))
				dMsg = a.decrypt()
				t = open('eTarget.txt', 'w')
				#t.write(dMsg)
				c = 0
				dMsg = dMsg.split('\n')
				print dMsg
				for i in dMsg:
					c += 1
					print "Decrypted Message(%s): %s" % (c, i)
					t.write(i + '\n')
				break
			else:
				print "Invalid input, try again!"


if __name__ == "__main__":
	runTest(sys.argv)