#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os, sys

from twobit.gitutil import GitRepo, GitMirror

def main():
    """ Test case to exercise the update function from the GitRepo object.
    """

    description = "Program to update an existing mirror of a git repo."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-g', '--gitdir', default='repo_mirror.git',
                        help="GIT_DIR where the mirror lives. This must " \
                             "already exist for this test.")
    parser.add_argument('-l', '--log-level', default='WARNING',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)  

    repo = GitRepo(gitdir=args.gitdir)
    repo = GitMirror(repo=repo)
    repo.update()

if __name__ == '__main__':
    main()
