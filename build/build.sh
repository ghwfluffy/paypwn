#!/bin/bash

set -eu -o pipefail

ENTRYPOINT=()
ARGS=()
if [ ${#} -gt 0 ]; then
    CMD="${1}"
    shift
    ENTRYPOINT=(--entrypoint "${CMD}")
    ARGS=("${@}")
fi

# Go to build script directory
BUILD_DIR="$(dirname $(readlink -f "${0}"))"
cd "${BUILD_DIR}"
source ../.env

# Build the build environment
docker build . --tag "paypwn-buildenv:${PAYPWN_VERSION}"

# Mount the source directory into the build environment and run it
cd ..
docker run \
    -ti \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    "${ENTRYPOINT[@]}" \
    "paypwn-buildenv:${PAYPWN_VERSION}" \
    "${ARGS[@]}"
if [ ${#ENTRYPOINT[@]} -gt 0 ]; then
    exit 0
fi

export DOCKER_BUILDKIT=1
docker build -t "paypwn:${PAYPWN_VERSION}" -f Dockerfile .
docker build -t "paypwn-devserver:${PAYPWN_VERSION}" -f devserver/Dockerfile .
docker build -t "paypwn-nginx:${PAYPWN_VERSION}" -f nginx/Dockerfile .
docker build -t "paypwn-postgres:${PAYPWN_VERSION}" -f database/Dockerfile .
