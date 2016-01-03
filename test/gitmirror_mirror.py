#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os, sys

from twobit.gitutil import GitRepo, GitMirror

def main():
    """ Test case to exercise the GitPoller.
    """

    description = "Program to mirror a git repo using the twobit.gitutil." \
                  "GitMirror object."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--remote', default='remote_repo.git',
                        help="URL of repo to clone")
    parser.add_argument('-c', '--mirror', default='repo_mirror.git',
                        help="directory to hold clone of remote")
    parser.add_argument('-l', '--log-level', default='WARNING',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)  

    repo = GitRepo(gitdir=args.mirror)
    mirror = GitMirror(remote=args.remote, repo=repo)
    mirror.mirror()

if __name__ == '__main__':
    main()
