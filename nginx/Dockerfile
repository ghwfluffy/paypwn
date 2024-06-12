FROM nginx:latest

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Ingress"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="nginx>\\w$ "

RUN set -eux; \
    rm -rf /etc/nginx; \
    true

COPY ./nginx/etc /etc/nginx

RUN set -eux; \
    chown -R root:root /etc/nginx; \
    true
