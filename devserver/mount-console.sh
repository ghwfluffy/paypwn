#!/bin/bash

set -eux -o pipefail

# Go to build script directory
TOPDIR="$(dirname $(readlink -f "${0}"))/.."
cd "${TOPDIR}"

source .env
docker run \
    -ti \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    --entrypoint ash \
    "paypwn-devserver:${PAYPWN_VERSION}" \

