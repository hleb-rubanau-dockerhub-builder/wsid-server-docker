import logging
from flask import Flask, request
import nacl.signing 
import nacl.public 
import nacl.encoding 
import os

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
app.logger.addHandler(logging.StreamHandler())

class WSID:
    def __init__(self, keybody):

        hexencoder=nacl.encoding.HexEncoder

        self.signing_key=nacl.signing.SigningKey(keybody,hexencoder)
        self.encryption_key=nacl.public.PrivateKey(keybody, hexencoder)

        # public keys as hex strings
        self.hexverify  = self.signing_key.verify_key.encode(hexencoder).decode()
        self.hexencpub  = self.encryption_key.public_key.encode(hexencoder).decode()
        self.verifyhash = str( hash( self.signing_key.verify_key ) )
        self.encpubhash = str( hash( self.encryption_key.public_key ) )


        app.logger.info("HEXVERIFY: %s" % hexverify)
        app.logger.info("HEXENCPUB: %s" % hexencpub)
        app.logger.info("VERIFYHASH: %s" % self.verifyhash)
        app.logger.info("ENCPUBHASH: %s" % self.encpubhash)

wsid=WSID(os.getenv("WSID_PRIVATE_KEY"))

@app.route("/")
def index():
    return get_public_keys() 

@app.route("/identity")
def get_public_keys():
    return { "verify": wsid.hexverify, "encrypt": wsid.hexencpub }

if __name__ == "__main__":
    app.run()
