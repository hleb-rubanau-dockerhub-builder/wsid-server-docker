import os
import logging
import json
from flask import Flask, request, abort
from base64 import b64decode
import requests 
from wsid.validation import validate_request

from wsid.client import WSIDClient

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

POLICY={
    '/allowed/.*$': [ 'http://127.0.0.1:887/*', ],
    '/allowedother/.*$': ['http://127.0.0.1:1887/*', ] # nonexisting
}

def validate(path, identity):
    for pathpattern, allowed in POLICY.items():
        app.logger.debug("CHECKING CONDITION: %s" % [pathpattern])
        if re.compile(pathpattern).match(subpath):
            app.logger.debug("CHECKING POLICY: %s" % allowed)
            for identity_pattern in allowed:
                app.logger.debug("CHECKING condition %s" % [identity_pattern])
                if re.compile(identity_pattern).match(identity):
                    app.logger.debug("MATCH FOUND!")
                    return True

    return False
            

# just an application that validates post payload
@app.route("/", methods=["POST"])
def index():
    return fallback('/')

@app.route('/<path:subpath>', methods=["POST"])
def fallback(subpath):
    identity, signature_payload, signature_claims = validate_request( request )
    app.logger.debug("IDENTITY=%s" % [identity])
    app.logger.debug("SIGNATURE=%s" % [validated_payload])
    app.logger.debug("CLAIMS=%s" % [signature_claims])
    
    if not validate(subpath, identity):
        app.logger.error("No access")
        abort(403)

    return { "result": "success" }

if __name__ == "__main__":
    app.run()
