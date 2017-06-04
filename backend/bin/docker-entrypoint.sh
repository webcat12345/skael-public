#!/bin/sh -e
exec uwsgi --master \
        --need-app \
        --module skael:app \
        --buffer-size 131072 \
        --processes 5 \
        --enable-threads \
        --chmod-socket=666 \
        --socket /var/run/backend/api/uwsgi.socket
