#!/bin/sh

# create repo that we can clone / poll
BASE=$(echo "$0" | sed 's&^\(.*\)\.sh&\1&')

# this will not return, must be killed with a ctrl-C
PYTHONPATH+=../src/ twistd --nodaemon --no_save --pidfile=${BASE}.pid --python=${BASE}.tac
