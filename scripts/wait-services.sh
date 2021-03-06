#!/usr/bin/env bash

set -ue

: "${DB_HOST:=postgresql}"
: "${DB_PORT:=5432}"


echo "Waiting for PostgreSQL server. Host ${DB_HOST}. Port ${DB_PORT}"
    timeout=15
    while ! nc -z ${DB_HOST} ${DB_PORT}; do
        timeout=$((timeout - 1))
        if [[ ${timeout} -eq 0 ]]; then
          echo 'Timeout! Exiting...'
          exit 1
        fi
        echo -n '.'
        sleep 1
    done
echo "PostgreSQL server ${DB_HOST}:${DB_PORT} is alive"
