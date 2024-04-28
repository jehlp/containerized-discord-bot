#!/bin/bash

usage() { echo "Usage: $0 [start|stop|restart]"; exit 1; }

start() { docker compose build --no-cache && docker compose up -d; }
stop() { docker compose down --rmi all --remove-orphans; }
restart() { stop && start; }

[[ $# -eq 0 ]] && usage

case "$1" in
    start|stop|restart) $1 ;;
    *) usage ;;
esac