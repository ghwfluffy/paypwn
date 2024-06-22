FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Ingress"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="nginx>\\w$ "

# Install nginx
RUN set -eux; \
    apk add --no-cache \
        nginx \
        ; \
    true

# Save mime types and remove all other configuration
RUN set -eux; \
    mv /etc/nginx/mime.types /tmp/; \
    rm -rf /etc/nginx; \
    true

# Copy nginx configuration
COPY ./nginx/etc /etc/nginx
COPY ./nginx/html /var/paypwn/html

# Restore mime types
RUN set -eux; \
    mv /tmp/mime.types /etc/nginx/mime.types; \
    true

# Set ownership
RUN set -eux; \
    chown -R root:root /etc/nginx; \
    chmod 0644 -R /etc/nginx; \
    true

# Remove unused files
RUN set -eux; \
    rm -rf /usr/share/nginx; \
    true

# Get paypwn front-end/build files
COPY ./paybuddy/vue /var/paypwn/paybuddy/vue
COPY ./shared/proto /var/paypwn/shared/proto
COPY ./paybuddy/proto /var/paypwn/paybuddy/proto
COPY ./setup /setup

# Protobuf build dependencies
RUN set -eux; \
    apk add --no-cache \
        build-base \
        npm \
        protobuf-dev \
        ; \
    true

# Build front-end
ENV NPM_CONFIG_TMP="npm"
ENV NPM_CONFIG_CACHE="npm"
ENV NPM_CONFIG_PREFIX="npm"
RUN set -eux; \
    cd /var/paypwn/paybuddy; /setup/setup-vite; \
    mv vue/dist www; \
    true

# Cleanup
RUN set -eux; \
    apk del --no-cache \
        build-base \
        npm \
        protobuf-dev \
        ; \
    rm -rf \
        /setup \
        /var/paypwn/paybuddy/proto \
        /var/paypwn/paybuddy/vue \
        ; \
    true

COPY ./nginx/bin/entrypoint /entrypoint
ENTRYPOINT ["/entrypoint"]
