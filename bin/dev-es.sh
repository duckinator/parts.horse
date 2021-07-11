#!/bin/sh -eu

trap 'rm -rf "$ES_HOME"' EXIT
export ES_HOME="$(mktemp -d)"
ES_BASE="$(dirname $(command -v elasticsearch))/.."

# Setup base directories
for dir in lib modules plugins; do
    ln -s "${ES_BASE}/${dir}" "${ES_HOME}/"
done

# Build ES config
mkdir "${ES_HOME}/config"
ln -s "$(dirname $0)/../config/elasticsearch.yml" "${ES_HOME}/config"

for file in jvm.options log4j2.properties; do
    cp "${ES_BASE}/config/${file}" "${ES_HOME}/config/"
done


elasticsearch
