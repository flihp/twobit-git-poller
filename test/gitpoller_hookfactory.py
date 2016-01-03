#!/usr/bin/env python

from argparse import ArgumentParser
import logging as log
import os

from twobit.gitutil import GitRepo, GitMirror, GitPoller
from twobit.buildbotutil import BuildbotHook, BuildbotHookFactory

def main():
    """ Test case to exercise the GitPoller hook script.
    """

    description = "Program to poll a git repo using the twobit.gitutil." \
                  "GitPoller object and its hook script functionality."
    parser = ArgumentParser(prog=__file__, description=description)
    parser.add_argument('-r', '--remote', default='remote.git',
                        help="URL of repo to clone")
    parser.add_argument('-g', '--gitdir', default='mirror.git',
                        help="directory to mirror remote into")
    parser.add_argument('-k', '--hook-script', default=None,
                        help="hook script")
    parser.add_argument('-l', '--log-level', default='WARNING', help="set log level")
    args = parser.parse_args()

    numeric_level = getattr(log, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(args.log_level))
    log.basicConfig(level=numeric_level)

    hook_config = { 'hook-script'   : args.hook_script,
                    'hook-logfile'  : 'gitpoller_hookfactory_script.log',
                    'hook-master'   : 'localhost',
                    'hook-port'     : '666',
                    'hook-user'     : 'test_user',
                    'hook-passwd'   : 'test_passwd',
                    'hook-projects' : '[ "test-project" ]' }
    repo = GitRepo(gitdir=args.gitdir)
    mirror = GitMirror(remote=args.remote,
                       repo=repo)
    hook_factory = BuildbotHookFactory()
    hook = hook_factory.make_buildbothook(config_dict=hook_config)
    poller = GitPoller(repo=repo,
                       mirror=mirror,
                       hook=hook)
    poller.poll()

if __name__ == '__main__':
    main()
