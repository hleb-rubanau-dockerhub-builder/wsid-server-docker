import os
import logging
import json
from flask import Flask, request, abort
from base64 import b64decode
import requests 
from wcid.requests import SignedRequests

from wsid.client import WSIDClient

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

API_ENDPOINT=os.getenv("API_ENDPOINT")
signed_requests=SignedRequests(os.getenv("WSID_ENDPOINT")

# just an application that validates post payload
@app.route("/", methods=["POST"])
def index():

    payload=request.get_data()
    path=request.path

    api_url = API_ENDPOINT+path
    app.logger("API_URL=%s" % api_url )

    return signed_requests.process('POST', api_url, data=payload).read()

if __name__ == "__main__":
    app.run()
