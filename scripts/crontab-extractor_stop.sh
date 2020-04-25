#!/usr/bin/env bash

RECORDER_PROCESS_NAME="puma-recorder"

# Stop recording and make sure all recording processes are really ended (since they can hang sometimes)
echo "Killing processes"
pkill -2 ${RECORDER_PROCESS_NAME}
sleep 3
pkill -2 ${RECORDER_PROCESS_NAME}
sleep 2
pkill -9 ${RECORDER_PROCESS_NAME}