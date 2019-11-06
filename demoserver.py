import os
import logging
import json
from flask import Flask, request, abort
from base64 import b64decode
import requests 
from wsid.requests import SignedRequests

from wsid.client import WSIDClient

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

API_ENDPOINT=os.getenv("API_ENDPOINT")
signed_requests=SignedRequests(os.getenv("WSID_ENDPOINT"))

# just an application that validates post payload
@app.route("/", methods=["POST"])
def index():
    return fallback('/')

@app.route('/<path:subpath>', methods=["POST"])
def fallback(subpath):
    payload=request.get_data()
    path=request.path

    api_url = API_ENDPOINT+path

    # convenient way to trigger usage scenarios
    if not('/unsigned/' in api_url):    
        app.logger.debug("Sending signed request to %s" % api_url)
        result = signed_requests.process('POST', api_url, data=payload, logger=app.logger)
    else:
        app.logger.debug("Sending unsigned request to %s" % api_url)
        result = requests.post(api_url, data=payload)

    if not result.ok:
        app.logger.error("Reraising error %s returned by API" % result.status_code)
        abort(result.status_code)

    return result.content

if __name__ == "__main__":
    app.run()
