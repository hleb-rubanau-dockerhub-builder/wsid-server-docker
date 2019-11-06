#!/bin/bash

set -e
set -o pipefail
set -x

token=$( curl -X POST -d '{"hello": "world"}' http://127.0.0.1:888/sign )

echo "token is $token, shoult be valid"
curl -X POST -d "$token" http://127.0.0.1:889/ 

echo "broken token is rejected"
curl -X POST -d "xxx$token" http://127.0.0.1:889/ 


echo "sleeping 11 seconds, outdated token will be rejected"
sleep 11
curl -X POST -d "$token" http://127.0.0.1:889/ 

