#!/bin/bash

set -e
set -o pipefail

if [ -z "$WSID_PRIVATE_KEY" ]; then
    export WSID_PRIVATE_KEY=$( /app/keygen.py )
fi

exec $*
