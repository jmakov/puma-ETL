#!/usr/bin/env bash


RECORDER_PROCESS_NAME="puma-recorder"

# Stop recording and make sure all recording processes are really ended (since they can hang sometimes)
echo "Killing processes"
pkill -2 ${RECORDER_PROCESS_NAME}
sleep 10
pkill -2 ${RECORDER_PROCESS_NAME}
sleep 10
pkill -9 ${RECORDER_PROCESS_NAME}

# Also exit network recording command. N.B. the process group (tcpdump ... | split --filter=before_split_cript) has to be exited by
# killing tcpdump first so that `before_split_cript` can finish and flush buffers.
pkill -2 gulp
sleep 10
pkill -2 gulp