#!/bin/bash

usage() {
    echo "Usage: $0 [--start|--stop|--restart]"
    exit 1
}

start() {
    docker build -t discord-bot .
    docker run -d --name my-bot --env-file ./conf/tokens.env discord-bot
}

stop() {
    docker stop my-bot
    docker rm my-bot
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
        stop
        start
        ;;
    *)
        usage
        ;;
esac
