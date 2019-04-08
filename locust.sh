#!/bin/bash

if [ -n "$1" ]; then
  FILE="$1"
else
  FILE="default.py"
fi

HOST=http://localhost:8000

. venv/bin/activate && ulimit -n 102400

for ((i=0;i<2;i++)); do
  locust --host=$HOST -f "locust_files/$FILE" --slave &
done

locust --host=$HOST -f "locust_files/$FILE" --master

killall -9 locust
