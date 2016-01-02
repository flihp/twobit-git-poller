#!/bin/sh

# create repo that we can clone / poll
BASE=$(echo "$0" | sed 's&^\(.*\)\.sh&\1&')
REPO_MIRROR=mirror.git
REPO_REMOTE=remote.git
REPO_WORK=${BASE}_work

repo_init () {
    local REPO_REMOTE=$1
    local REPO_WORK=$2

    mkdir ${REPO_REMOTE}
    git init --bare ${REPO_REMOTE}
    git clone ${REPO_REMOTE} ${REPO_WORK}
}

# write a file in a git work-tree then push it to the remote so the
# poller will know
repo_commit () {
    local REPO_WORK=$1
    local FILE=$2
    local BRANCH=${3:master}

    while read LINE; do
        echo ${LINE}
    done > ${REPO_WORK}/${FILE}

    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} add ${FILE}
    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} commit --all \
        --message "test commit"
    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} push origin ${BRANCH}
}

# remove files created by the test script
trap '{ rm -rf "${REPO_REMOTE}" "${REPO_WORK}" "${REPO_MIRROR}" "${BASE}.pid"; }' 0 2 3

# create a new repo. We will be polling this git repo
repo_init ${REPO_REMOTE} ${REPO_WORK}

# add a test file & commit
echo "test0" | { repo_commit ${REPO_WORK} test_file0; }
# add another file & commit
echo "test1" | { repo_commit ${REPO_WORK} test_file1; }

# this will not return, must be killed with a ctrl-C
PYTHONPATH+=../src/ twistd --nodaemon --no_save --pidfile=${BASE}.pid --python=${BASE}.tac
