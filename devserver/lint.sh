#!/bin/bash

set -eu -o pipefail

# --no-cache        always rebuild docker
# --console         drop into shell
# --fix             automatically fix lint/format issues
CHECK_CACHE=1
INTERACTIVE=(-t)
CMD=(-c 'cd paybuddy/vue && npm install && npm run lint-format')
while [ ${#} -gt 0 ]; do
    if [ "${1}" == "--no-cache" ]; then
        CHECK_CACHE=0
        shift
    elif [ "${1}" == "--console" ]; then
        INTERACTIVE+=(-i)
        CMD=()
        shift
    elif [ "${1}" == "--fix" ]; then
        for i in "${!CMD[@]}"; do
            CMD[$i]="${CMD[$i]//lint/relint}"
            CMD[$i]="${CMD[$i]//format/reformat}"
        done
        shift
    else
        echo "Invalid argument ${1}." 1>&2
        exit 1
    fi
done

# Go to build script directory
TOPDIR="$(dirname $(readlink -f "${0}"))/.."
cd "${TOPDIR}"

# Get environment
source .env

# Build docker
if [ ${CHECK_CACHE} -eq 0 ] || ! docker image ls | grep paypwn-devserver | grep "${PAYPWN_VERSION}" > /dev/null; then
    BUILDKIT_INLINE_CACHE=1 docker build -f ./devserver/Dockerfile -t "paypwn-devserver:${PAYPWN_VERSION}" .
fi

# Run linter container
docker run \
    "${INTERACTIVE[@]}" \
    --workdir "$(pwd)" \
    -v "$(pwd):$(pwd):rw" \
    -v "/etc/passwd:/etc/passwd:ro" \
    --user "$(id -u)" \
    --entrypoint ash \
    "paypwn-devserver:${PAYPWN_VERSION}" \
    "${CMD[@]}"
