#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os
import sys

from twobit.gitutil import GitHubOrg

def main():
    """ Test case to exercise the GitHubOrg get_repo_urls function.
    """

    description = "Program to poll a GitHub Org for its repositories " \
                  "using the twobit.gitutil.GitHubOrg get_repo_urls " \
                  "function."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-n', '--name', default='OpenXT',
                        help="GitHub organization name")
    parser.add_argument('-l', '--log-level', default='WARNING',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    log.info("Creating a GitHubOrg object for Org: {0}".format(args.name))
    org = GitHubOrg(args.name)
    repo_git_urls = org.get_repo_git_urls()
    log.info("Polled github org {0} and got {1} repo urls: {2}"
             .format(args.name, len(repo_git_urls), repo_git_urls))

if __name__ == '__main__':
    main()
