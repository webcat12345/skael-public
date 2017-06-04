FROM node:8.0.0

# nginx binaries installation
# Taken from https://github.com/nginxinc/docker-nginx/blob/c769ad8ab21dfb374fa33d8fb9d0822d0fa8d2e5/mainline/stretch/Dockerfile

ENV NGINX_VERSION 1.13.1-1~jessie
ENV NJS_VERSION   1.13.1.0.1.10-1~jessie

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y gnupg \
    && \
    NGINX_GPGKEY=573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62; \
    found=''; \
    for server in \
        ha.pool.sks-keyservers.net \
        hkp://keyserver.ubuntu.com:80 \
        hkp://p80.pool.sks-keyservers.net:80 \
        pgp.mit.edu \
    ; do \
        echo "Fetching GPG key $NGINX_GPGKEY from $server"; \
        apt-key adv --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$NGINX_GPGKEY" && found=yes && break; \
    done; \
    test -z "$found" && echo >&2 "error: failed to fetch GPG key $NGINX_GPGKEY" && exit 1; \
    echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
                        nginx=${NGINX_VERSION} \
                        nginx-module-xslt=${NGINX_VERSION} \
                        nginx-module-geoip=${NGINX_VERSION} \
                        nginx-module-image-filter=${NGINX_VERSION} \
                        nginx-module-njs=${NJS_VERSION} \
                        gettext-base \
    && apt-get install --no-install-recommends --no-install-suggests -y \
                        python3 \
                        python3-jinja2 \
    && rm -rf /var/lib/apt/lists/*

# frontend app build

WORKDIR /skael
ADD skael/package.json .
RUN npm install
ENV PATH="/skael/node_modules/.bin:${PATH}"

ADD skael/ /skael
RUN ng build --target=production --environment=prod

# nginx configuration

ADD bin /usr/local/bin

ADD nginx /etc/nginx

CMD ["/usr/local/bin/docker-entrypoint.sh"]
EXPOSE 80
