#!/usr/bin/env bash
mkdir -p .up
while read line ; do
  echo '{"date": "'`date`'","message": "'$line'"}'>.up-event.log
done < $0
