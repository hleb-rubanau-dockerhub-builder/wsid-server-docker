import logging
from flask import Flask, request
from nacl.signing import SigningKey
from nacl.public import PrivateKey
from nacl.encoding import HexEncoder

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
app.logger.addHandler(logging.StreamHandler())

class WSID:
    def __init__(keybody):
        self.signing_key=SigningKey(keybody,HexEncoder)
        self.encryption_key=PrivateKey(keybody, HexEncoder)

        # public keys as hex strings
        self.hexverify  = self.signing_key.verify_key.encode(HexEncoder).decode()
        self.hexencpub  = self.encryption_key.public_key.encode(HexEncoder).decode()
        self.verifyhash = self.__hash__.encode(HexEncoder).decode()
        self.encpubhash = self.__hash__.encode(HexEncoder).decode()


        app.logger.info("HEXVERIFY: %s" % hexverify)
        app.logger.info("HEXENCPUB: %s" % hexencpub)
        app.logger.info("VERIFYHASH: %s" % self.verifyhash)
        app.logger.info("ENCPUBHASH: %s" % self.encpubhash)

if __name__ == "__main__":
    app.run()
