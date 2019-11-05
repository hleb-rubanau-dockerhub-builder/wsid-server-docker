import os
import logging
import wsid
from flask import Flask, request

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)

@app.route("/")
def index():
    data=request.get_data()
    identity, payload, claims = wsid.validate( data )
    
    return { "payload": json.loads( b64decode( payload.encode() ) ),
             "signed_by": identity,
             "expires": claims['exp']}
     

if __name__ == "__main__":
    app.run()
