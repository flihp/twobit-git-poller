#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os
import sys

from twobit.gitutil import GitHubOrg

def main():
    """ Test case to exercise the GitPoller hook script.
    """

    description = "Program to poll a GitHub Org for its repositories " \
                  "using the twobit.gitutil.GitHubOrg poll_repos."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-n', '--name', default='OpenXT',
                        help="")
    parser.add_argument('-l', '--log-level', default='WARNING', help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    log.info("Creating a GitHubOrg object for Org: {0}".format(args.name))
    org = GitHubOrg(args.name)
    repos = org.get_repos()
    print("Polled github org {0} and got repo urls: {1}".format(args.name, repos))

if __name__ == '__main__':
    main()
