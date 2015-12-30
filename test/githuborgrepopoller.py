#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log

from twobit.gitutil import GitHubOrg, GitHubOrgRepoPoller

def mycallback(url=None):
    if url is not None:
        log.info("mycallback: {0}".format(url))
    else:
        log.error("mycallback passed no URL :(")

def main():
    """ Test case to exercise the GitHubOrgRepoPoller and its callback
        mechanism.
    """
    description = "Program to poll a GitHub Org for its repositories " \
                  "using the twobit.gitutil.GitHubOrgRepoPoller and its " \
                  "callback function."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-n', '--name', default='OpenXT',
                        help="GitHub organization name")
    parser.add_argument('-l', '--log-level', default='INFO',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    log.info("Creating a GitHubOrg object for Org: {0}".format(args.name))
    org = GitHubOrg(args.name)
    log.info("Creating a GitHubOrgRepoPoller for Org object: {0}"
             .format(id(org)))
    org_poller = GitHubOrgRepoPoller(org=org, callback=mycallback)
    org_poller.poll()

if __name__ == '__main__':
    main()
