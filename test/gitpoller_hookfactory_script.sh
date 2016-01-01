#!/bin/sh

LOGFILE=gitpoller_hook_script.log
{
    echo "$0 invoked with paramters: $@"
    echo "  and environment:"
    printenv
} > ${LOGFILE} 2>&1

while read DATA; do
    echo "${DATA}"
done > ${LOGFILE} 2>&1
