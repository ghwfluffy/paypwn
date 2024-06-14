FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Front-end Hot-Reload Development Server"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="devserver>\\w$ "

ENV NPM_CONFIG_TMP="npm"
ENV NPM_CONFIG_CACHE="npm"
ENV NPM_CONFIG_PREFIX="npm"

# Dependencies
RUN set -eux; \
    apk add --no-cache \
        nginx \
        npm \
        ; \
    true

# Copy nginx configuration
COPY ./devserver/etc/nginx.conf /etc/nginx/nginx.conf
COPY ./devserver/etc/forward_api.conf /etc/nginx/forward_api.conf
COPY ./devserver/etc/forward_dev.conf /etc/nginx/forward_dev.conf

COPY ./devserver/bin/entrypoint /entrypoint
ENTRYPOINT ["/entrypoint"]
