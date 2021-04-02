from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64
import logging
import codecs

logger = logging.getLogger(__name__)


class Nazgul(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def encrypt(self):
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=init_vector)
        encrypted_data = cipher.encrypt(pad(self.data, AES.block_size))
        encrypted_data_with_iv = base64.b64encode(cipher.iv + encrypted_data)
        return encrypted_data_with_iv

    def decrypt(self):
        init_vector = self.data[:AES.block_size]
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=init_vector)
        decrypted_data = unpad(cipher.decrypt(self.data[AES.block_size:]), AES.block_size)
        return decrypted_data