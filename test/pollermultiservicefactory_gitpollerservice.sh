#!/bin/sh

# create repo that we can clone / poll
BASE=$(echo "$0" | sed 's&^\(.*\)\.sh&\1&')
REPO_REMOTE_0=remote0.git
REPO_REMOTE_1=remote1.git
REPO_WORK_0=${BASE}_work_0
REPO_WORK_1=${BASE}_work_1
DELETES="${REPO_REMOTE_0} ${REPO_REMOTE_1} ${REPO_WORK_0} ${REPO_WORK_1} mirror0.git mirror1.git"

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
trap '{ rm -rf ${DELETES}; }' 0 2 3

# create a new repo. We will be polling this git repo
repo_init ${REPO_REMOTE_0} ${REPO_WORK_0}
repo_init ${REPO_REMOTE_1} ${REPO_WORK_1}

# add a test file & commit
echo "remote0_test0" | { repo_commit ${REPO_WORK_0} remote0_test_file0; }
echo "remote1_test0" | { repo_commit ${REPO_WORK_1} remote1_test_file0; }

# add test files and commit
echo "remote0_test1" | { repo_commit ${REPO_WORK_0} remote0_test_file1; }
echo "remote1_test1" | { repo_commit ${REPO_WORK_1} remote1_test_file1; }

# this will not return, must be killed with a ctrl-C
PYTHONPATH=../src twistd --nodaemon --no_save --pidfile=${BASE}.pid --python=${BASE}.tac
