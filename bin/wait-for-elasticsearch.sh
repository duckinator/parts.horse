#!/bin/bash

MAX_DELAY=30

function finish() {
  printf "$1 Done!\n"
  exit
}

function fail() {
  echo
  echo "Elasticsearch was not available within ${MAX_DELAY} seconds. Aborting."
  exit 1
}

if [ -z "${ELASTICSEARCH}" ]; then
  ELASTICSEARCH="http://localhost:9200"
fi

printf "Waiting for Elasticsearch to become available..."

for ((i=0; i<=$MAX_DELAY; i++)); do
  if [ "$VERBOSE" == "true" ]; then
    curl "${ELASTICSEARCH}" && finish "\n"
  else
    curl "${ELASTICSEARCH}" &>/dev/null && finish
    printf .
  fi
  sleep 1
done

fail
