#!/usr/bin/env bash

function handleSigChld() {
  python3 -u ./up.py 2>&1 | ./up-log.sh up
}
trap handleSigChld SIGCHLD
set -o monitor

python3 -u ./up.py 2>&1 | ./up-log.sh up


