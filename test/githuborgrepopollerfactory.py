#!/usr/bin/env python

from argparse import ArgumentParser
import logging
import os

from twobit.gitutil import GitHubOrgRepoPollerFactory

def callback(remote=None, org=None):
    """
    """
    logging.info("callback got remote: {0} from github org: {1}"
                 .format(remote, org._orgname))

def main():
    """ Test case to exercise the GitHubOrgRepoPollerFactory
    """
    description = ""
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-l', '--log-level', default='INFO',
                        help="set log level")
    parser.add_argument('-o', '--org', default='openxt',
                        help="GitHub org name")
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    logging.basicConfig(level=numeric_level)

    config = { 'name' : args.org }

    log = logging.getLogger(__name__)
    ghorp_factory = GitHubOrgRepoPollerFactory()
    log.info("Getting poller from factoy: {0}".format(id(ghorp_factory)))
    poller = ghorp_factory.make_poller(config_dict=config,
                                       callback=callback)
    log.info("Got poller {0}, polling ...".format(id(poller)))
    poller.poll()

if __name__ == '__main__':
    main()
