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
        build-base \
        nginx \
        npm \
        protobuf-dev \
        sudo \
        ; \
    true

# Allow nginx to run as sudo
RUN set -eux; \
    echo 'ALL ALL=NOPASSWD: /usr/sbin/nginx' >> /etc/sudoers.d/00-nginx; \
    chmod 0440 /etc/sudoers.d/00-nginx; \
    true

# Copy nginx configuration
COPY ./devserver/etc/nginx.conf /etc/nginx/nginx.conf
COPY ./devserver/etc/forward_api.conf /etc/nginx/forward_api.conf
COPY ./devserver/etc/forward_dev.conf /etc/nginx/forward_dev.conf
COPY ./devserver/etc/forward_histoire.conf /etc/nginx/forward_histoire.conf
COPY ./devserver/etc/forward_histoire_api.conf /etc/nginx/forward_histoire_api.conf

# Build protobufs
COPY ./shared/proto /var/paypwn/shared/proto
COPY ./paybuddy/vue /var/paypwn/paybuddy/vue
COPY ./paybuddy/proto /var/paypwn/paybuddy/proto
COPY ./setup/setup-vite /setup/setup-vite
RUN set -eux; \
    cd /var/paypwn/paybuddy; \
    /setup/setup-vite dev; \
    true

COPY ./devserver/bin/entrypoint /entrypoint
ENTRYPOINT ["/entrypoint"]
