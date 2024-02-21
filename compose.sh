#!/usr/bin/env sh

cd $(dirname ${0})

if [[ "${1}" == 'dev' ]]; then
  shift
  COMMAND="-f docker-compose.yml -f docker-compose.dev.yml"
fi

if [[ "${1}" == 'run' ]]; then
  shift
  COMMAND="${COMMAND} run --rm"
fi

if [[ "${1}" == 'manage.py' ]]; then
  shift
  COMMAND="${COMMAND} server python manage.py"
fi

docker compose ${COMMAND} ${@}
