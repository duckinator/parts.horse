#!/bin/bash

if [ -n "$1" ]; then
  FILE="$1"
else
  FILE="default.py"
fi

. venv/bin/activate && ulimit -n 20480 && locust --host=http://localhost:5000 -f "locust_files/$FILE"
