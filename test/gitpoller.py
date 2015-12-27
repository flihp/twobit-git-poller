#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os
import sys

from twobit.gitutil import GitRepo, GitMirror, GitPoller

def main():
    """ Test case to exercise the GitPoller.
    """

    description = "Program to poll a git repo using the twobit_gitpoller." \
                  "GitPoller object."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--remote', default='remote.git',
                        help="URL of repo to clone")
    parser.add_argument('-g', '--gitdir', default='mirror.git',
                        help="directory to mirror remote into")
    parser.add_argument('-b', '--basedir', default=os.getcwd(),
                        help="directory to check out repo into")
    parser.add_argument('-l', '--log-level', default='WARNING', help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)
    repo = GitRepo(gitdir=args.gitdir)
    mirror = GitMirror(remote=args.remote,
                       repo=repo)

    poller = GitPoller(basedir=args.basedir,
                       repo=repo,
                       mirror=mirror)
    poller.poll()

if __name__ == '__main__':
    main()
