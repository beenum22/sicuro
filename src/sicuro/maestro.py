from .nazgul import Nazgul
import os
import base64
import binascii
import logging
from colorama import Fore, Style

logger = logging.getLogger(__name__)


class Maestro(object):

    def __init__(self, key=None, key_byte_size=32, output_dir='~/sicuro_data/'):
        self.key = key
        self.key_byte_size = key_byte_size
        self.output_dir = output_dir

    def _create_work_directory(self):
        try:
            logger.debug("Creating output directory '%s'", self.output_dir)
            os.makedirs(os.path.expanduser(self.output_dir))
        except FileExistsError:
            logger.warning("Target output directory '%s' already exists", self.output_dir)
        except OSError:
            logger.error("Failed to create the target '%s' output directory", self.output_dir)
            raise

    def _is_file_type_data_source(self, data_source):
        if data_source and os.path.exists(os.path.expanduser(data_source)):
            logger.info("Target data source '%s' is a file path", data_source)
            return True
        return False

    def _parse_input_data(self, data_source=None):
        logger.debug("Parsing input target data '%s'", data_source)
        if not data_source:
            logger.warning("No input target string or file path found")
            data = input("Enter the message you want to encrypt/decrypt: ").encode()
        elif self._is_file_type_data_source(data_source):
            data = self._read_file(data_source)
        else:
            logger.info("Parsing target as an input string instead of a file path")
            data = bytes(data_source,'utf-8')
        return data

    def _read_file(self, file):
        try:
            logger.debug("Reading target file '%s'", file)
            with open(file, 'rb') as myfile:
                data = myfile.read()
            return data
        except IOError:
            logger.error("Failed to open target file '%s'", file)
            raise

    def _create_file(self, data, file_path):
        try:
            logger.debug("Creating target output file '%s'", file_path)
            abs_path = os.path.expanduser(file_path)
            with open(abs_path, 'wb') as t:
                t.write(data)
        except Exception:
            raise

    def _remove_files(self, *args):
        try:
            logger.debug("Removing target file/s '%s'", args)
            for file in args:
                abs_path = os.path.expanduser(file)
                if os.path.exists(abs_path):
                    os.remove(abs_path)
        except Exception:
            raise

    def _encrypt_data(self, data):
        logger.debug("Initializing input target data encryption")
        self.generate_key(overwrite=False)
        self.validate_key()
        nazgul = Nazgul(self.key, data)
        encrypted_data = nazgul.encrypt()
        return encrypted_data

    def _decrypt_data(self, data):
        logger.debug("Initializing input target data decryption")
        if not self.key:
            self.key = input("Enter the key: ")
        self.validate_key()
        nazgul = Nazgul(self.key, base64.b64decode(data))
        decrypted_data = nazgul.decrypt()
        return decrypted_data

    def _save_output(self, data, id=None):
        if not id:
            id = "target.txt"
        logger.debug("Save data in '%s' file", id)
        self._create_work_directory()
        self._create_file(data, os.path.join(self.output_dir, id))

    def _sanitize_key(self):
        try:
            logger.debug("Sanitizing encryption key")
            if type(self.key) == str:
                logger.debug("Encryption key is of type 'str'. Converting to 'bytes'")
                self.key = base64.b64decode(self.key)
        except binascii.Error as err:
            logger.error("Encryption key sanitization failed")
            logger.error("Failed to decode the encryption key from Base64 format")
            raise Exception("Failed to decode the encryption key from Base64 format [%s]" % err)

    def validate_key(self):
        try:
            assert self.key is not None, "Encryption key not found"
            assert type(self.key) in [str, bytes], "Invalid encryption key type. Only 'str' and 'bytes' types are allowed"
            self._sanitize_key()
            assert len(self.key) == self.key_byte_size, "Invalid encryption key size. Make sure the encryption key byte size is equal to '%d'" % self.key_byte_size
        except AssertionError:
            logger.error("Encryption key validation failed")
            raise

    def generate_key(self, overwrite=False):
        if self.key:
            logger.warning("Encryptionadd key already exists")
            if not overwrite:
                logger.warning("Overwriting encryption key disabled")
                return False
        logger.debug("Generating random encryption key")
        self.key = os.urandom(self.key_byte_size)
        return True

    def lock_data(self, data_path=None, store=False):
        try:
            data = self._parse_input_data(data_path)
            encrypted_data = self._encrypt_data(data)
            if store and self._is_file_type_data_source(data_path):
                self._save_output(encrypted_data, id=os.path.basename(data_path))
            elif store and not self._is_file_type_data_source(data_path):
                self._save_output(encrypted_data, id="locked_data.txt")
            return encrypted_data
        except AssertionError:
            raise
        except Exception as err:
            logger.error("Failed to secure the target data")
            raise

    def unlock_data(self, data_path=None, store=False):
        try:
            data = self._parse_input_data(data_path)
            decrypted_data = self._decrypt_data(data)
            if store and self._is_file_type_data_source(data_path):
                self._save_output(decrypted_data, id=os.path.basename(data_path))
            elif store and not self._is_file_type_data_source(data_path):
                self._save_output(decrypted_data, id="unlocked_data.txt")
            return decrypted_data
        except AssertionError:
            raise
        except Exception as err:
            logger.error("Failed to unlock the target data")
            raise

    def get_key(self):
        return base64.b64encode(self.key)

    def display_key(self):
        print(f"{Fore.LIGHTYELLOW_EX}WARNING: {Fore.YELLOW}Please save this key at a secure location as it will be needed for decryption{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}Key: {Fore.LIGHTWHITE_EX}%s{Style.RESET_ALL}" % str(self.get_key(), 'utf-8'))

    def display_data(self, data):
        # print("\n")
        if len(data) > 1024*5:
            print(f"{Fore.LIGHTYELLOW_EX}WARNING: {Fore.YELLOW}Data length is greater than '1024' characters. Data output display will be truncated to '1024' characters. Make sure to add --save flag to persist data in a file.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}Data: {Fore.LIGHTWHITE_EX}%s (Truncated){Style.RESET_ALL}" % str(data, 'utf-8')[:1024*5])
        else:
            print(f"{Fore.LIGHTCYAN_EX}Data: {Fore.LIGHTWHITE_EX}%s{Style.RESET_ALL}" % str(data, 'utf-8'))