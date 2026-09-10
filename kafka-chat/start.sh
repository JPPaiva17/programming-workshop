#!/bin/bash
check_result() {
    local resultado=$1
    if [[ $resultado -ne 0 ]]; then exit $resultado; fi
    echo
}

./stop.sh

sudo docker compose build
check_result $?

sudo docker compose up -d
check_result $?

sudo docker ps -a

cd frontend/
python3 -m http.server --bind 0.0.0.0 8000