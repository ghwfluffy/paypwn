#!/bin/bash

set -eux -o pipefail

export COMPOSE_PROJECT_NAME=paypwn-tests

cleanup() {
    docker compose down -v
}
trap cleanup EXIT TERM INT HUP

# Start dockers
RATE_LIMIT_ENABLED=false \
    docker compose \
        -f docker-compose.yml \
        -f devserver/docker-compose.tests.yml \
        up -d
sleep 2

# Get nginx IP
IP="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
        "$(docker compose ps | grep nginx | awk '{print $1}')"
    )"

# Run tests
docker compose exec \
    -w /var/paypwn/paybuddy/vue \
    -e API_BASE_URL="http://${IP}/paybuddy/api" \
    devserver \
    npm run test
