#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 [--start|--stop]"
    exit 1
fi

if [[ $1 == "--start" ]]; then
    docker build -t discord-bot .
    docker run -d --name my-bot --env-file ./tokens.env discord-bot
elif [[ $1 == "--stop" ]]; then
    docker stop my-bot
    docker rm my-bot
else
    echo "Invalid option. Usage: $0 [--start|--stop]"
    exit 1
fi