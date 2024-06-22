#!/bin/bash

set -eu -o pipefail

# --no-cache        always rebuild docker
# --console         drop into shell
CHECK_CACHE=1
INTERACTIVE=(-t)
CMD=(-c "cd paybuddy; $(pwd)/setup/run-mypy")
while [ ${#} -gt 0 ]; do
    if [ "${1}" == "--no-cache" ]; then
        CHECK_CACHE=0
        shift
    elif [ "${1}" == "--console" ]; then
        INTERACTIVE+=(-i)
        CMD=()
        shift
    fi
done

# Go to build script directory
TOPDIR="$(dirname $(readlink -f "${0}"))/.."
cd "${TOPDIR}"

# Get environment
source .env

# Build docker
if [ ${CHECK_CACHE} -eq 0 ] || ! docker image ls | grep paypwn-mypy | grep "${PAYPWN_VERSION}" > /dev/null; then
    BUILDKIT_INLINE_CACHE=1 docker build -f ./devserver/Dockerfile.mypy -t "paypwn-mypy:${PAYPWN_VERSION}" .
fi

# Run linter container
docker run \
    "${INTERACTIVE[@]}" \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    --entrypoint ash \
    "paypwn-mypy:${PAYPWN_VERSION}" \
    "${CMD[@]}"
