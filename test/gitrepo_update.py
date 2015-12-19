#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os, sys

from twobit.gitutil import GitRepo

def main():
    """ Test case to exercise the update function from the GitRepo object.
    """

    description = "Program to update an existing mirror of a git repo."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--remote', default='remote_repo.git',
                        help="URL of repo to clone")
    parser.add_argument('-m', '--mirror', default='repo_mirror.git',
                        help="directory to hold clone of remote")
    parser.add_argument('-l', '--log-level', default='WARNING',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)  

    repo = GitMirror(remote=args.remote, mirror=args.clone)
    repo.update()

if __name__ == '__main__':
    main()
