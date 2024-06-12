FROM postgres:16

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Database"

ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="postgres>\\w$ "

RUN set -eux; \
    mkdir -p /docker-entrypoint-initdb.d; \
    true

COPY ./database/init.sql /docker-entrypoint-initdb.d/init-db.sql

RUN set -eux; \
    chown -R root:root /docker-entrypoint-initdb.d; \
    true

VOLUME /var/lib/postgresql/data
