#!/bin/sh

MAX_DELAY=300 # 5 minutes

finish() {
  echo
  printf "Done!\n"
  exit
}

fail() {
  echo
  echo "Elasticsearch was not available within ${MAX_DELAY} seconds. Aborting."
  exit 1
}

if [ -z "${ELASTICSEARCH}" ]; then
  ELASTICSEARCH="http://localhost:9200"
fi

echo "Waiting for Elasticsearch to become available..."

i=0
while [ $i -le $MAX_DELAY ]; do
  if [ "$VERBOSE" = "true" ]; then
    curl "${ELASTICSEARCH}" && finish
  else
    curl "${ELASTICSEARCH}" && finish
  fi
  sleep 1
  i=$((i + 1))
done

fail
