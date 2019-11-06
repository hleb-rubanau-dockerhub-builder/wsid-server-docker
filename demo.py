import os
import logging
import json
import wsid
from flask import Flask, request, abort
from base64 import b64decode

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

# just an application that validates post payload
@app.route("/", methods=["POST"])
def index():
    payload=request.get_data()
    app.logger.debug("DATA=%s" % [payload])

    try:
        identity, payload, claims = wsid.validate( payload, app.logger )
    except wsid.InvalidTimestamps:
        abort(403, "Token outdated")
    except wsid.InvalidSignature:
        abort(403, "Malformed token")
    
    app.logger.debug("IDENTITY=%s" % [identity])
    
    return { "payload": json.loads( b64decode( payload ) ),
             "signed_by": identity,
             "expires": claims['exp']}
     

if __name__ == "__main__":
    app.run()
