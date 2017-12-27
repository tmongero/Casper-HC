from Crypto.Cipher import AES
from Crypto import Random
import base64


class AESCipher(object):
    """
    This class will encrypt and decrypt strings from a database object
    Block size is 16
    Encryption key must be 32 bytes in length
    """
    def __init__(self, key):
        self.key = str(key)

    def encrypt(self, raw):
        print(raw, len(raw), 'first')
        raw = self._pad(raw)
        print(raw, len(raw))
        iv = Random.new().read(AES.block_size)
        print(iv, len(iv))
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        print(cipher)
        print(base64.b64encode(iv + cipher.encrypt(raw)), len(base64.b64encode(iv + cipher.encrypt(raw))))
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[16:]))

    @staticmethod
    def _pad(raw):
        return raw + (AES.block_size - len(raw) % AES.block_size) * chr(AES.block_size - len(raw) % AES.block_size)

    @staticmethod
    def _unpad(padded):
        return padded[:-ord(padded[len(padded) - 1:])]


def main():

    pass

if __name__ == "__main__":
    main()
