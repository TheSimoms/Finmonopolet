#!/bin/bash
set -xe

sed -i "s|API_HOST|$API_HOST|g" /usr/share/nginx/html/**.js

exec "$@"
