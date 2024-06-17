#!/bin/bash

set -eu -o pipefail

# Go to build script directory
TOPDIR="$(dirname $(readlink -f "${0}"))/.."
cd "${TOPDIR}"

source .env
docker run \
    -t \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    --entrypoint ash \
    "paypwn-devserver:${PAYPWN_VERSION}" \
    -c 'cd paybuddy/vue && npm install && npm run lint-format'
