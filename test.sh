#!/bin/bash

set -e
set -o pipefail
set -x

CLIENT_ENDPOINT=http://127.0.0.1:889

curl -X POST -d '{"hello": "world"}' $CLIENT_ENDPOINT/allowed/method

curl -X POST -d '{"should": "fail"}' $CLIENT_ENDPOINT/disallowed/method

