#!/bin/bash

set -e
set -o pipefail
set -x

curl -X POST -d '{"hello": "world"}' http://127.0.0.1:888/allowed 

curl -X POST -d '{"should": "fail"}' http://127.0.0.1:888/disallowed 

