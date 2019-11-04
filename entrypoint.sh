#!/bin/bash

set -e
set -o pipefail

if [ -z "$WSID_PRIVATE_KEY" ]; then
    export WSID_PRIVATE_KEY=$( /usr/bin/python3 /app/keygen.py | tee /dev/shm/debug.txt )

    cat /dev/shm/debug.txt
fi

exec $*
