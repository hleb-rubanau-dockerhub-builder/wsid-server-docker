import os
import json
import logging
from datetime import datetime

from flask import Flask, request

import nacl.signing 
import nacl.public 
import nacl.encoding 
import nacl.hash


LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
#app.logger.addHandler(logging.StreamHandler())

def is_like_b64(msg):
    return msg.replace('=','').isalnum()

class WSID:
    def __init__(self, keybody, identity, ttl=10):

        hexencoder=nacl.encoding.HexEncoder

        self.signing_key=nacl.signing.SigningKey(keybody,hexencoder)
        self.encryption_key=nacl.public.PrivateKey(keybody, hexencoder)

        self.manifest = {
            "sig":   self.signing_key.verify_key.encode(hexencoder).decode(),
            "enc":   self.encryption_key.public_key.encode(hexencoder).decode()
        }

        self.identity = identity
        self.ttl      = ttl
        self.logger   = app.logger # <- bad
        #sigbytes=self.signing_key.verify_key.encode(hexencoder) 
        #app.logger.info("HASH blake2b: %s" % nacl.hash.blake2b( sigbytes, digest_size=4 ) )
   
    def sign(self, message):
        
        message = message.decode() if isinstance(message,bytes) else message

        b64=nacl.encoding.Base64Encoder
        hexenc=nacl.encoding.HexEncoder

        now=int(datetime.utcnow().timestamp())
        claims = {
            'iss': self.identity,
            'iat': now,
            'exp': now + self.ttl
        }
        claims_b64 = b64.encode(json.dumps(claims).encode()).decode()
         
        payload=message + "." + claims_b64

        self.logger.debug("PAYLOAD: %s" % payload)
            
        signed = self.signing_key.sign(payload.encode())
        sigstring = hexenc.encode( signed.signature ).decode()
        
        return payload+"."+sigstring

wsid=WSID(os.getenv("WSID_PRIVATE_KEY"), os.getenv("WSID_IDENTITY"))

@app.route("/")
def index():
    return get_public_keys() 

@app.route("/manifest")
def get_public_keys():
    return wsid.manifest

@app.route("/sign", methods=["POST"])
def sign_data():
    payload = request.get_data()
    if not is_like_b64(payload.decode()):
        payload = nacl.encoding.Base64Encoder.encode(payload)
    
    return wsid.sign( payload )

if __name__ == "__main__":
    app.run()
