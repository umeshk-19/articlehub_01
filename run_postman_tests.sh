#!/usr/bin/env bash
set -x

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

APIURL=${APIURL:-http://localhost:4000/api}

npx newman run $SCRIPTDIR/postman_tests.json \
  --delay-request 500 \
  --global-var "APIURL=$APIURL" \