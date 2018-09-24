from nazgul import Nazgul
import os
import base64
import logging
from zizou import Zizou

logger = logging.getLogger(__name__)


class Maestro(object):

    def __init__(self, bL, output_dir='~/sicuro_data/'):
        self.bL = bL
        self.output_dir = output_dir
        self.master_key = None
        self.master_dic = {}
        Zizou._create_dir(self.output_dir)

    def encrypt_maestro(self, key=None, data_path=None):
        output_file = 'target.txt'
        key_file = 'key.txt'
        try:
            if data_path:
                data_path = Zizou.get_abs_path(data_path)
                assert os.path.exists(data_path), "Input data file does not exist"
                data = self._read_file(data_path)
                output_file = os.path.basename(data_path)
            else:
                data = raw_input("Enter the message you want to encrypt: ")
            assert data != None, "No data source provided"
            key, encrypted_data = self._encrypt_data(data, key)
            self._create_file(encrypted_data, os.path.join(self.output_dir, output_file))
            #self._create_file(key, os.path.join(self.output_dir, key_file))
            return key, encrypted_data
            #self._display_output(key=key, data=encrypted_data)
        except AssertionError as e:
            raise

    def decrypt_maestro(self, data_path=None, key=None, store=False):
        output_file = 'target.txt'
        try:
            if data_path:
                assert os.path.exists(data_path), "Input data file does not exist"
                data = self._read_file(data_path)
                output_file = os.path.basename(data_path)
            else:
                data = raw_input("Enter the message you want to decrypt: ")
            if not key:
                key = raw_input("Enter the key: ")
            assert data != None, "No data source provided"
            assert key != None, "No key source provided"
            data = self._decrypt_data(key, data)
            if data_path:
                self._remove_files(data_path)
            if store is True:
                self._create_file(data, os.path.join(self.output_dir, output_file))
            #self._display_output(data=data)
            return data
        except AssertionError as e:
            raise

    def _gen_master_key(self):
        return os.urandom(self.bL)

    def _encrypt_keys(self):
        pass

    def _store_keys(self):
        pass

    def _read_file(self, file):
        try:
            with open(file, 'r') as myfile:
                data = myfile.read()
            return data
        except IOError as e:
            raise

    def _encrypt_data(self, data, key=None):
    	if key:
    		key = base64.b64decode(key)
    	else:
	        key = os.urandom(self.bL)
        print key
        a = Nazgul(key, data, self.bL)
        encrypted_data = a.encrypt()
        key = base64.b64encode(key)
        return key, encrypted_data

    def _decrypt_data(self, key, data):
        a = Nazgul(base64.b64decode(key), base64.b64decode(data))
        decrypted_data = a.decrypt()
        count = 0
        decrypted_data = decrypted_data.split('\n')
        for i in decrypted_data:
            count += 1
        return decrypted_data

    def _create_file(self, data, file_path):
        try:
            abs_path = Zizou.get_abs_path(file_path)
            with open(abs_path, 'w') as t:
                if type(data) != list:
                    data = data.split('\n')
                for line in data:
                    if line == data[-1]:
                        t.write(line)
                    else:
                        t.write(line + '\n')
        except:
            raise

    def _remove_files(self, *args):
        try:
            for file in args:
                abs_path = Zizou.get_abs_path(file)
                if os.path.exists(abs_path):
                    os.remove(abs_path)
        except:
            raise

    def display_output(self, key=None, data=None):
    	print "=========================="
        if key:
            print "----|Key|----"
            print key
        print "=========================="    
        if data:
            print "----|Data|----"
            print str(data)
        print "=========================="







