#!/bin/sh

# create repo that we can clone / poll
BASE=$(echo "$0" | sed 's&^\(.*\)\.sh&\1&')
REPO_REMOTE=${BASE}.git
REPO_MIRROR=${BASE}_mirror.git
REPO_WORK=${BASE}_work
BASE_DIR=$(pwd)
HOOK_SH=${BASE}_script.sh

repo_init () {
    local REPO_REMOTE=$1
    local REPO_WORK=$2

    mkdir ${REPO_REMOTE}
    git init --bare ${REPO_REMOTE}
    git clone ${REPO_REMOTE} ${REPO_WORK}
}

repo_mirror () {
    local REPO_REMOTE=$1
    local REPO_MIRROR=$2

    git clone --mirror ${REPO_REMOTE} ${REPO_MIRROR}
}

# create new branch in REPO_WORK and push to remote
repo_branch () {
    local REPO_WORK=$1
    local BRANCH=$2

    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} checkout -b ${BRANCH}
    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} push origin ${BRANCH}
}

# write a file in a git work-tree then push it to the remote so the
# poller will know
repo_commit () {
    local REPO_WORK=$1
    local FILE=$2
    local BRANCH=${3:-master}

    while read LINE; do
        echo ${LINE}
    done > ${REPO_WORK}/${FILE}

    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} add ${FILE}
    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} commit --all \
        --message "test commit"
    git --git-dir=${REPO_WORK}/.git --work-tree=${REPO_WORK} push origin ${BRANCH}
}

repo_poll () {
    local REPO_REMOTE=$1
    local BASE_DIR=$2
    local REPO_MIRROR=$3
    local HOOK_SH=$4

    if [ -d ${REPO_MIRROR} ]; then
        echo "REPO_MIRROR: ${REPO_MIRROR} exists!"
    fi

    PYTHONPATH=../src/ ./${BASE}.py --gitdir=${REPO_MIRROR} --basedir=${BASE_DIR} --remote=${REPO_REMOTE} --hook-script=${HOOK_SH} --log-level=DEBUG
    if [ $? -ne 0 ]; then
        echo "TEST FAILED"
        exit $?
    fi
}

# create a new repo. We will be polling this git repo
repo_init ${REPO_REMOTE} ${REPO_WORK}

# add a test file & commit
echo "test0" | { repo_commit ${REPO_WORK} test_file0; }

# add a new branch
repo_branch ${REPO_WORK} "test_branch"
echo "blarg0" | { repo_commit ${REPO_WORK} blarg_file0 "test_branch"; }
repo_mirror ${REPO_REMOTE} ${REPO_MIRROR}

# add another file & commit
echo "test1" | { repo_commit ${REPO_WORK} test_file1; }
echo "blarg1" | { repo_commit ${REPO_WORK} blarg_file1 "test_branch"; }
# one more time for good measure
echo "Polling ${REPO_REMOTE}"
repo_poll ${REPO_REMOTE} ${BASE_DIR} ${REPO_MIRROR} ${HOOK_SH}

# if we get this far the test passed
echo "test passed: cleaning up"
rm -rf ${REPO_REMOTE} ${REPO_WORK} ${REPO_MIRROR}
