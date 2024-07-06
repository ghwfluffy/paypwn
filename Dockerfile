FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="paypwn>\\w$ "

# Copy web files
COPY ./shared/python /var/paypwn/shared/python
COPY ./shared/proto /var/paypwn/shared/proto
COPY ./paybuddy/python /var/paypwn/paybuddy/python
COPY ./paybuddy/proto /var/paypwn/paybuddy/proto
COPY ./setup /setup

# Dependencies
RUN set -eux; \
    apk add --no-cache \
        build-base \
        postgresql16-client \
        postgresql16-dev \
        protobuf-dev \
        py3-virtualenv \
        python3 \
        python3-dev \
        ; \
    # Setup python runtime environment
    cd /var/paypwn/paybuddy; \
        /setup/setup-venv; \
    # Entrypoint
    cp -v /setup/entrypoint /var/paypwn/; \
    # Cleanup
    rm -rf /setup /root/.cache; \
    for eph in mypy .mypy_cache proto mypy.ini; do \
        find /var/paypwn \( -path '*/venv' -prune \) -and -name "${eph}" | { \
            while read f; do rm -rf "${f}"; done; \
        }; \
    done ; \
    find /var/paypwn -name __pycache__ | { \
        while read f; do rm -rf "${f}"; done; \
    }; \
    apk del \
        build-base \
        postgresql16-dev \
        protobuf-dev \
        py3-virtualenv \
        python3-dev \
        ; \
    true

# Expose the fastcgi apps
EXPOSE \
    8080 \
    8081 \
    8082 \
    8083

ENTRYPOINT ["/var/paypwn/entrypoint"]
