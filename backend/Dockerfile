FROM python:3.6.1

RUN apt-get update && \
    apt-get install -y \
        libpq-dev \
        && \
    rm -rf /var/lib/apt/lists/*

RUN pip install virtualenv
RUN python -m virtualenv /virtualenv
ENV PATH="/virtualenv/bin:${PATH}"

WORKDIR /skael
ADD skael/requirements.txt .
RUN pip install -r requirements.txt

ADD skael/ /skael

ADD bin /usr/local/bin

CMD ["/usr/local/bin/docker-entrypoint.sh"]
