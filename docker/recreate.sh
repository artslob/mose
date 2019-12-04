#!/usr/bin/env bash

# full directory name of the script no matter where it is being called from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DIR="${DIR%/}"

compose_file="${DIR}/docker-compose.yml"

docker-compose -f "$compose_file" exec db bash -c '/scripts/recreate-db.sh'
docker-compose -f "$compose_file" run --rm web bash -c "./manage.py migrate && ./manage.py populate_db"
