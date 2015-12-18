#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os
import sys

from twobit_gitpoller import GitPoller

def main():
    """ Test case to exercise the GitPoller.
    """

    description = "Program to poll a git repo using the twobit_gitpoller." \
                  "GitPoller object."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument("-u", "--url", default="repo_clone.git",
                        help="URL of repo to clone")
    parser.add_argument("-b", "--basedir", default=os.getcwd(),
                        help="directory to check out repo into")
    parser.add_argument("-k", "--hook", default=None,
                        help="hook script called when git repo changes")
    parser.add_argument('-l', '--log-level', default='WARNING', help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    poller = GitPoller(repo_url=args.url,
                       basedir=args.basedir,
                       hook=args.hook)
    try:
        poller.poll()
    except Exception as excep:
        log.error("caught exception from poller.poll(): {0}".format(excep))
        sys.exit(1)

if __name__ == '__main__':
    main()
