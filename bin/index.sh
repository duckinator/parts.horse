#!/bin/sh -e

# Make things work on FreeBSD even if $PATH isn't set up for Python.
export PATH="$PATH:$HOME/.local/bin"
cd $(realpath $(dirname $0))/..

if [ -z "${ELASTICSEARCH}" ]; then
  ELASTICSEARCH="http://localhost:9200"
fi

curl() {
  if [ -z "$VERBOSE" ]; then
    command curl -s -H "Content-Type: application/json" "$@" >/dev/null
  else
    command curl -H "Content-Type: application/json" "$@"
  fi
}

cd config

# Delete the index, if it exists.
curl -XDELETE "${ELASTICSEARCH}/parts"

# Create the index, with the current config.
curl -XPUT "${ELASTICSEARCH}/parts" --data-binary "@elasticsearch-analyzer-config.json"

cd ../parts

# Populate the index.
for file in *.json; do
  name=$(echo $file | sed 's/.json$//')
  curl -XPOST "${ELASTICSEARCH}/parts/_doc/${name}" --data-binary "@${file}"
done
