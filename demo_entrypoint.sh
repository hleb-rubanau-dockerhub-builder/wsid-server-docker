#!/bin/bash

pip3 install requests

# strict binding to 127.0.0.1 
export GUNICORN_CMD_ARGS="${GUNICORN_CMD_ARGS} --bind 127.0.0.1:$GUNICORN_PORT"

exec $*
