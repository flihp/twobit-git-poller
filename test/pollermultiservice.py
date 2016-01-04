#!/usr/bin/env python

from argparse import ArgumentParser
import logging, sys

from twobit.buildbotutil import BuildbotHookFactory
from twobit.gitutil import GitPollerFactory
from twobit.twisted_gitpoller import PollerMultiServiceFactory

def main():
    """ Test case to exercise the PollerMultiServiceFactory
    """
    description = "Program to poll multiple git repositories by way of " \
                  "the PollerMultiServiceFactory."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-c', '--config-file', default='config.ini',
                        help="Configuration file.")
    parser.add_argument('-l', '--log-level', default='INFO',
                        help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    logging.basicConfig(level = numeric_level)
    log = logging.getLogger(__name__)
    log.info("Making PollerMultiServiceFactory with config file: {0}"
             .format(args.config_file))

    pmsf = PollerMultiServiceFactory()
    pms = pmsf.makeService(options={ 'config' : args.config_file })
    pms.startService()

if __name__ == '__main__':
    main()
