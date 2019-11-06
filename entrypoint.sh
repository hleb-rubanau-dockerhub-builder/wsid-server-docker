#!/bin/bash

set -e
set -o pipefail

function say() { echo "$*" >&2 ; }
function die() { say "ERROR: $*" ; exit 1 ; }

if [ -z "$WSID_PRIVATE_KEY" ]; then
    say "Generating WSID_PRIVATE_KEY" 
    export WSID_PRIVATE_KEY=$( python3 -e 'import wsid; print(wsid.new_private_key())' )
    if [ -z "$WSID_PRIVATE_KEY" ]; then die "No private key generated!" ; fi
else
    say "WSID_PRIVATE_KEY contains predefined key, doing no regeneration"
fi

# strict binding to 127.0.0.1 
export GUNICORN_CMD_ARGS="${GUNICORN_CMD_ARGS} --bind 127.0.0.1:$GUNICORN_PORT"

exec $*
