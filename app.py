import logging
from flask import Flask, request

LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
app = Flask(__name__)
app.logger.setLevel(LOG_LEVEL)
app.logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    app.run()
