#!/bin/bash

set -eu -o pipefail

# Go to build script directory
TOPDIR="$(dirname $(readlink -f "${0}"))/.."
cd "${TOPDIR}"

# --no-cache option rebuild docker
CHECK_CACHE=1
if [ ${#} -gt 0 ]; then
    if [ "${1}" == "--no-cache" ]; then
        CHECK_CACHE=0
    fi
fi

source .env
if [ ${CHECK_CACHE} -eq 0 ] || ! docker image ls | grep paypwn-mypy | grep "${PAYPWN_VERSION}" > /dev/null; then
    BUILDKIT_INLINE_CACHE=1 docker build -f ./devserver/Dockerfile.mypy -t "paypwn-mypy:${PAYPWN_VERSION}" .
fi
docker run \
    -t \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    --entrypoint ash \
    "paypwn-mypy:${PAYPWN_VERSION}" \
    -c "cd paybuddy; $(pwd)/setup/run-mypy"
