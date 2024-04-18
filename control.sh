#!/bin/bash

usage() {
    echo "Usage: $0 [--start|--stop|--restart]"
    exit 1
}

start() {
    docker compose build --no-cache
    docker-compose up -d 
}

stop() {
    docker-compose down
}

restart() {
    docker-compose down
    docker compose build --no-cache
    docker-compose up -d
}

if [[ $# -eq 0 ]]; then
    usage
fi

case "$1" in
    --start)
        start
        ;;
    --stop)
        stop
        ;;
    --restart)
        restart
        ;;
    *)
        usage
        ;;
esac