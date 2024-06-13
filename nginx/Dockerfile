FROM nginx:latest

LABEL maintainer="GhwFluffy <ghw@ghwfluffy.com>"
LABEL description="PayPwn Ingress"

ENV LANG="en_US.utf8"
ENV LANGUAGE="en_US:en"

ENV PS1="nginx>\\w$ "

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
