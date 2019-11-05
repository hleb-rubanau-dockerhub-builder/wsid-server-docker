#!/bin/bash

set -e
set -o pipefail
set -x

token=$( curl -X POST -d {"hello": "world"} http://127.0.0.1:888/sign )

echo "token is $token"

curl -X POST -d "$token" http://127.0.0.1:889/ 


