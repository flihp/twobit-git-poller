#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os, sys

from twobit.gitutil import GitRepo

def main():
    """ Test case to translate a git symbolic name to its hash """

    description = "Program to get a git hash from a symbolic name."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--repo', default='repo.git',
                        help="git directory")
    parser.add_argument('-i', '--symname', default='refs/heads/master',
                        help="symbolic name to get hash for")
    parser.add_argument('-l', '--log-level', default='WARNING',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)  

    repo = GitRepo(gitdir=args.repo)
    print("hash for git symbolic name: {0} is: {1}"
          .format(args.symname, repo.get_hash(args.symname)))

if __name__ == '__main__':
    main()
