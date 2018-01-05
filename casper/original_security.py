from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib


class AESCipher(object):
    """
    This class will encrypt and decrypt strings from a database object
    Block size is 16
    Encryption key must be 32 bytes in length
    """
    def __init__(self, key):
        self.block_size = 32
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, raw):
        return raw + (self.block_size - len(raw) % self.block_size) * chr(self.block_size - len(raw) & self.block_size)

    @staticmethod
    def _unpad(padded):
        return padded[:-ord(padded[len(padded)-1:])]


def main():

    pass

if __name__ == "__main__":
    main()
