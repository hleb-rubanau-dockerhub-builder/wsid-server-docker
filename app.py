import os
import logging
from base64 import b64encode
from datetime import datetime

from flask import Flask, request
from wsid import WSID

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
#app.logger.addHandler(logging.StreamHandler())

def is_like_b64(msg):
    return msg.replace('=','').isalnum()


wsid=WSID(  os.getenv("WSID_PRIVATE_KEY"), 
            os.getenv("WSID_IDENTITY"), 
            logger=app.logger
            )

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
        payload = b64encode(payload)
    
    return wsid.sign( payload )

if __name__ == "__main__":
    app.run()
