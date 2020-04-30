#!/bin/bash

# Make things work on FreeBSD even if $PATH isn't set up for Python.
export PATH="$PATH:$HOME/.local/bin"

cd $(realpath $(dirname $0))/..

cd config
curl -H "Content-Type: application/json" -XPUT "localhost:9200/parts" --data-binary "@elasticsearch-analyzer-config.json"

cd ../parts

for file in *.json; do
  name=$(echo $file | sed 's/.json$//')
  curl -H "Content-Type: application/json" -XPOST "localhost:9200/parts/_doc/${name}" --data-binary "@${file}"
  echo
done
