#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os

from twobit.gitutil import GitPollerFactory

def main():
    """ Test case to exercise the GitPollerFactory
    """

    description = "Program to create a GitPoller from the provided " \
                  "configuration dictionary"
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-b', '--basedir', default=os.getcwd(),
                        help="directory to check out repo into")
    parser.add_argument('-g', '--gitdir', default='mirror.git',
                        help="directory to use as gitdir for mirror")
    parser.add_argument('-r', '--remote', default='remote.git',
                        help="URL of repo to clone")
    parser.add_argument('-l', '--log-level', default='INFO',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    conf = { 'basedir' : args.basedir,
             'gitdir' : args.gitdir,
             'url' : args.remote }
    factory = GitPollerFactory()
    poller = factory.make_poller(config_dict=conf)
    log.info("GitPollerFactory made GitPoller with id: {0}"
             .format(id(poller)))
    poller.poll()

if __name__ == '__main__':
    main()
