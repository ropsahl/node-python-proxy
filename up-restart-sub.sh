#!/usr/bin/env bash
dummyPid=-1

function handleSigChld() {
 echo '['`date`']['$dummyPid'] exit:  bash ./dummy.sh'>> .up-event.log
 bash ./dummy.sh &
 dummyPid=$!
 echo '['`date`']['$dummyPid'] start: bash ./dummy.sh'>> .up-event.log

}
trap handleSigChld SIGCHLD
set -o monitor

bash ./dummy.sh &
dummyPid=$!
wait


