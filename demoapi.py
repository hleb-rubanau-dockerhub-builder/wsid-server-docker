import os
import logging
import json
from flask import Flask, request, abort
from base64 import b64decode
import requests 
from wsid.validation import validate_request

from wsid.client import WSIDClient
from wsid.exceptions import WSIDValidationError
from wsid.policy import SimplePolicy

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

policy = SimplePolicy( 
                        {
                            '/allowed/.*$': [ '^http://127.0.0.1:888/', ],
                            '/allowedother/.*$': ['^http://127.0.0.1:1887/', ] # nonexisting
                        }, 
                        logger=app.logger 
                     )

def flask_auth(subpath):
    try:
        identity, signature_payload, signature_claims = validate_request( request, logger=app.logger )
        if not policy.allowed(subpath, identity):
            raise WSIDValidationError("Access prohibited")
    except WSIDValidationError as e:
        app.logger.error("VALIDATION FAILED: %s" % e)
        abort(403)
    

# just an application that validates post payload
@app.route("/", methods=["POST"])
def index():
    return fallback('/')

@app.route('/<path:subpath>', methods=["POST"])
def fallback(subpath):
    flask_auth(subpath)
    return { "result": "success" }

if __name__ == "__main__":
    app.run()
