#!/bin/sh

# Make things work on FreeBSD even if $PATH isn't set up for Python.
export PATH="$PATH:$HOME/.local/bin"

cd $(realpath $(dirname $0))/..

# Basically, take everything after 'web: ' and run it.
$(cat Procfile | cut -d ' ' -f 2-)
