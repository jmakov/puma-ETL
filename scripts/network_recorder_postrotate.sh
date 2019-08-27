#!/usr/bin/env bash

# gulp sends file name as an argumen to this script (tcpdump -z)
IN_FN=$1
TMP_FN=$IN_FN.tmp
FIN_FN=$IN_FN.zst

zstd -q -T4 -1 --rm $IN_FN -o $TMP_FN
# signal with an atomic rename that the file is not being written to anymore
mv $TMP_FN $FIN_FN
