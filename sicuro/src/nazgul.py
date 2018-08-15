from Crypto import Random
from Crypto.Cipher import AES
import base64
import logging

logger = logging.getLogger(__name__)


class Nazgul(object):
    def __init__(self, key, msg, bL=32):
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
        #print base64.b64encode(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dMsg = cipher.decrypt(self.msg[AES.block_size:]).rstrip('{')
        # print dMsg
        return dMsg