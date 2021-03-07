#!/usr/bin/env bash

TEMPLATES_PATH=/tmp/scripts
NGINX_TEMPLATE="${TEMPLATES_PATH}/nginx.conf.template"
NGINX_CONFIG="/etc/nginx/conf.d/default.conf"

sed -e 's#${BACKEND}#'"${BACKEND}"'#g' -e \
    's#${BACKEND_PORT}#'"${BACKEND_PORT}"'#g' -e \
    's#${PORT}#'"${PORT}"'#g' -e \
    's#${HOST}#'"${HOST}"'#g' -e \
    's#${ROOT}#'"${ROOT}"'#g' < ${NGINX_TEMPLATE} > ${NGINX_CONFIG}
