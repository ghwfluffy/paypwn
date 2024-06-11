FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Build Environment"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

# Build tools
RUN set -eux; \
    apk add --no-cache \
        npm \
        protobuf-dev \
        ; \
    true

COPY ./entrypoint /entrypoint

ENV NPM_CONFIG_TMP="npm"
ENV NPM_CONFIG_CACHE="npm"
ENV NPM_CONFIG_PREFIX="npm"

ENTRYPOINT ["/entrypoint"]
