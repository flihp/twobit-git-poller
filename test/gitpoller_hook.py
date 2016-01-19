#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os
import sys

from twobit.gitutil import GitRepo, GitMirror, GitPoller
from twobit.buildbotutil import BuildbotHook

def main():
    """ Test case to exercise the GitPoller hook script.
    """

    description = "Program to poll a git repo using the twobit.gitutil." \
                  "GitPoller object and the twobit.buildbotutil." \
                  "BuildbotHook object hook script functionality."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--remote', default='remote.git',
                        help="URL of repo to clone")
    parser.add_argument('-g', '--gitdir', default='mirror.git',
                        help="directory to mirror remote into")
    parser.add_argument('-b', '--basedir', default=os.getcwd(),
                        help="directory to check out repo into")
    parser.add_argument('-k', '--hook-script', default=None,
                        help="hook script")
    parser.add_argument('-l', '--log-level', default='WARNING', help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)
    repo = GitRepo(gitdir=args.gitdir)
    mirror = GitMirror(remote=args.remote,
                       repo=repo)
    hook = BuildbotHook(script=args.hook_script,
                        host='localhost',
                        port='666',
                        user='test_user',
                        passwd='test_passwd',
                        projects=[ 'test_project0',
                                   'test_project1',
                                   'test_project2' ],
                        logfile='test_logfile.log')
    poller = GitPoller(repo=repo,
                       mirror=mirror,
                       hook=hook)
    poller.poll()

if __name__ == '__main__':
    main()
