#!/bin/sh -e

# Make things work on FreeBSD even if $PATH isn't set up for Python.
export PATH="$PATH:$HOME/.local/bin"

cd $(realpath $(dirname $0))/..

./bin/wait-for-elasticsearch.sh

./bin/index.sh

python3.7 ./lib/render.py

exec hypercorn app:app
