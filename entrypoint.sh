#!/bin/bash

set -e
set -o pipefail

function say() { echo "$*" >&2 ; }
function die() { say "ERROR: $*" ; exit 1 ; }

if [ -z "$WSID_PRIVATE_KEY" ]; then
    say "Generating WSID_PRIVATE_KEY" 
    export WSID_PRIVATE_KEY=$( /app/keygen.py )
    if [ -z "$WSID_PRIVATE_KEY" ]; then die "No private key generated!" ; fi
else
    say "WSID_PRIVATE_KEY contains predefined key, doing no regeneration"
fi

exec $*
