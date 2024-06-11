FROM alpine:3

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

# Dependencies
RUN set -eux; \
    apk add --no-cache \
        postgresql16-client \
        python3 \
        py3-virtualenv \
        ; \
    true

# Copy web files
COPY ./paybuddy/vue/dist /var/paypwn/paybuddy/www
COPY ./paybuddy/python /var/paypwn/paybuddy/python
COPY ./paybuddy/api /var/paypwn/paybuddy/api

# Setup runtime environment
COPY setup /setup
RUN set -eux; \
    /setup/setup-venv; \
    cp -v /setup/entrypoint /var/paypwn/; \
    rm -rf /setup; \
    true

# Expose the fastcgi apps
EXPOSE \
    8080 \
    8081 \
    8082 \
    8083

ENTRYPOINT ["/var/paypwn/entrypoint"]
