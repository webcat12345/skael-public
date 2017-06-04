#!/bin/sh -e
/usr/local/bin/process_nginx_template /etc/nginx/nginx.conf.jinja2 /etc/nginx/nginx.conf
exec nginx -g "daemon off;"
