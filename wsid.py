import logging
from flask import Flask, request
import nacl.signing 
import nacl.public 
import nacl.encoding 
import nacl.hash
import os

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
#app.logger.addHandler(logging.StreamHandler())

class WSID:
    def __init__(self, keybody):

        hexencoder=nacl.encoding.HexEncoder

        self.signing_key=nacl.signing.SigningKey(keybody,hexencoder)
        self.encryption_key=nacl.public.PrivateKey(keybody, hexencoder)

        self.manifest = {
            "sig":   self.signing_key.verify_key.encode(hexencoder).decode(),
            "enc":   self.encryption_key.public_key.encode(hexencoder).decode()
        }

        sigbytes=self.signing_key.verify_key.encode(hexencoder) 
        app.logger.info("HASH blake2b: %s" % nacl.hash.blake2b( sigbytes, digest_size=4 ) )
    
    def sign(self, message):
        signed = self.signing_key.sign(message)
        return { 
                 "msg": signed.message.decode(),
                 "sig": nacl.encoding.HexEncoder.encode(signed.signature).decode()
                }

wsid=WSID(os.getenv("WSID_PRIVATE_KEY"))

@app.route("/")
def index():
    return get_public_keys() 

@app.route("/manifest")
def get_public_keys():
    return wsid.manifest

@app.route("/sign", methods=["POST"])
def sign_data():
    # todo: inject ttl, expiration -- maybe envelope?
    result = wsid.sign( request.get_data() )
    app.logger.debug("RESULT=%s" % result)
    return result

if __name__ == "__main__":
    app.run()
