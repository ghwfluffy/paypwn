FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="paypwn>\\w$ "

# Dependencies
RUN set -eux; \
    apk add --no-cache \
        build-base \
        npm \
        postgresql16-client \
        postgresql16-dev \
        protobuf-dev \
        py3-virtualenv \
        python3 \
        python3-dev \
        ; \
    true

# Copy web files
COPY ./paybuddy/vue /var/paypwn/paybuddy/vue
COPY ./paybuddy/python /var/paypwn/paybuddy/python
COPY ./shared/python /var/paypwn/shared/python
COPY ./paybuddy/proto /var/paypwn/paybuddy/proto
COPY ./shared/proto /var/paypwn/paybuddy/proto/paypwn
COPY ./mypy.ini /var/paypwn/paybuddy/
COPY ./setup /setup

# Build front-end
ENV NPM_CONFIG_TMP="npm"
ENV NPM_CONFIG_CACHE="npm"
ENV NPM_CONFIG_PREFIX="npm"
RUN set -eux; \
    cd /var/paypwn/paybuddy; /setup/setup-vite; \
    mv vue/dist www; \
    true

# Setup python runtime environment
RUN set -eux; \
    cd /var/paypwn/paybuddy; /setup/setup-venv; \
    /setup/setup-mypy; \
    true

# Lint python
RUN set -eux; \
    cd /var/paypwn/paybuddy; /setup/run-mypy; \
    true

# Entrypoint
RUN set -eux; \
    cp -v /setup/entrypoint /var/paypwn/; \
    true

# Cleanup
RUN set -eux; \
    cd /var/paypwn/paybuddy; \
    rm -rf proto protopy/mypy vue mypy.ini .mypy_cache; \
    rm -rf /setup; \
    apk del \
        build-base \
        npm \
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
