#!/bin/bash

# Make things work on FreeBSD even if $PATH isn't set up for Python.
export PATH="$PATH:$HOME/.local/bin"
cd $(realpath $(dirname $0))/..

if [ -z "${ELASTICSEARCH}" ]; then
  ELASTICSEARCH="http://localhost:9200"
fi

./bin/wait-for-elasticsearch.sh

cd config

# Delete the index, if it exists.
curl -H "Content-Type: application/json" -XDELETE "${ELASTICSEARCH}/parts"

# Create the index, with the current config.
curl -H "Content-Type: application/json" -XPUT "${ELASTICSEARCH}/parts" --data-binary "@elasticsearch-analyzer-config.json"

cd ../parts

# Populate the index.
for file in *.json; do
  name=$(echo $file | sed 's/.json$//')
  curl -H "Content-Type: application/json" -XPOST "${ELASTICSEARCH}/parts/_doc/${name}" --data-binary "@${file}"
  echo
done
