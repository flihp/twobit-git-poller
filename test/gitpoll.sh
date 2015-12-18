#!/bin/sh

# create repo that we can clone / poll
BASE=$(echo "$0" | sed 's&^\(.*\)\.sh&\1&')
REPO_DIR=${BASE}.git
REPO_TMP=${BASE}_tmp
BASE_DIR=${BASE}_test

repo_init () {
    local REPO_DIR=$1
    local REPO_TMP=$2

    mkdir ${REPO_DIR}
    git init --bare ${REPO_DIR}
    git clone ${REPO_DIR} ${REPO_TMP}
}

# write a file in a git work-tree 
repo_commit () {
    local REPO_TMP=$1
    local FILE=$2
    local BRANCH=${3:master}

    while read LINE; do
        echo ${LINE}
    done > ${REPO_TMP}/${FILE}

    git --git-dir=${REPO_TMP}/.git --work-tree=${REPO_TMP} add ${FILE}
    git --git-dir=${REPO_TMP}/.git --work-tree=${REPO_TMP} commit --all \
        --message "test commit"
    git --git-dir=${REPO_TMP}/.git --work-tree=${REPO_TMP} push origin ${BRANCH}
}

repo_poll () {
    local REPO_DIR=$1
    local BASE_DIR=$2

    PYTHONPATH=../src ${BASE}.py --url=${REPO_DIR} --basedir=${BASE_DIR} --log=DEBUG
    if [ $? -ne 0 ]; then
        echo "TEST FAILED"
        exit $?
    fi
}

# create a new repo. We will be polling this git repo
repo_init ${REPO_DIR} ${REPO_TMP}

# poll it: this will clone an empty repo
echo "Polling ${REPO_DIR}: first"
repo_poll ${REPO_DIR} ${BASE_DIR}

# add a test file & commit
echo "test0" | { repo_commit ${REPO_TMP} test_file0; }
# poll again: we should get the new file
echo "Polling ${REPO_DIR}: second"
repo_poll ${REPO_DIR} ${BASE_DIR}

# add another file & commit
echo "test1" | { repo_commit ${REPO_TMP} test_file1; }
# one more time for good measure
echo "Polling ${REPO_DIR}: third"
repo_poll ${REPO_DIR} ${BASE_DIR}

# if we get this far the test passed
echo "test passed: cleaning up"
rm -rf ${REPO_DIR} ${REPO_TMP} ${BASE_DIR}
