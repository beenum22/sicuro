#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Beenum'
__version__ = '3.0'

import argparse
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
        # print base64.b64encode(iv)
        eMsg = base64.b64encode(iv + cipher.encrypt(pad(self.msg)))
        return eMsg

    def decrypt(self):

        iv = self.msg[:AES.block_size]
        print base64.b64encode(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dMsg = cipher.decrypt(self.msg[AES.block_size:]).rstrip('{')
        # print dMsg
        return dMsg


class runTest(object):

    def __init__(self, argv):
        usage = ('python %prog <add variables here>')
        workDir = os.path.dirname(os.path.realpath(__file__))
        bL = 32
        parser = argparse.ArgumentParser(
            description='Main Code.', version=__version__)
        parser.add_argument(
            "task",
            help="Select Encryption/Decryption.",
            choices=['E','D']
            )
        parser.add_argument(
        	"--save",
        	help="Save the decrypted output.",
        	action='store_true'
        	)
        parser.add_argument(
            "-t", "--target", default='%s/target.txt' % workDir, 
            help="Target file source path."
            )
        parser.add_argument(
            "-k", "--key", default='%s/key.txt' % workDir,
            help="Key file source path."
            )
        args = parser.parse_args()
        if args.task == 'E':
            if os.path.exists("target.txt") is True:
                with open('target.txt', 'r') as myfile:
                    msg = myfile.read()
            else:
                msg = raw_input("Enter the message you want to encrypt: ")
            key = os.urandom(bL)
            print "Encryption key: %s" % base64.b64encode(key)
            a = ED(key, msg, bL)
            eMsg = a.encrypt()
            print "Encrypted Message: %s" % (eMsg)
            # print eMsg
            k = open('key.txt', 'w')
            k.write(base64.b64encode(key) + '\n')
            t = open('target.txt', 'w')
            t.write(eMsg)
        elif args.task == 'D':
            if os.path.exists("target.txt") is True:
                with open('target.txt', 'r') as myfile:
                    msg = myfile.read()
            else:
                msg = raw_input("Enter the message you want to encrypt: ")

            if os.path.exists("key.txt") is True:
                key = list(open('key.txt', 'r'))[0].strip('\n')
            else:
                key = raw_input("Enter the key (optional): ")
            print "Encryption key given is: %s" % key
            a = ED(base64.b64decode(key), base64.b64decode(msg))
            dMsg = a.decrypt()
            c = 0
            dMsg = dMsg.split('\n')
            for i in dMsg:
                c += 1
                print "Decrypted Message(%s): %s" % (c, i)
            if os.path.exists("target.txt") is True:
                os.remove('target.txt')
            if os.path.exists("key.txt") is True:
                os.remove('key.txt')
            if args.save is True:
                t = open('target.txt', 'w')
                for i in dMsg:
                    if i == dMsg[-1]:
                        t.write(i)
                    else:
	                    t.write(i + '\n')
                t.close() 

if __name__ == "__main__":
    runTest(sys.argv)
