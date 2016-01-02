#!/usr/bin/env python

from argparse import ArgumentParser
import logging as plog
import ast, os

from twisted.application.service import Application
from twisted.python import log as tlog

from twobit.buildbotutil import BuildbotHookFactory
from twobit.gitutil import GitPollerFactory, GitPollerServiceFactory

""" Test TAC file / program to exercise the GitPollerService
"""

# configuration for the GitPollerService
config_dict = {
    'basedir' : os.getcwd(),
    'gitdir' : 'mirror.git',
    'url' : 'remote.git',
    'log-level' : 'INFO',
    'poll-interval' : '30',
    'hook-logfile' : './hook.log',
    'hook-master' : 'localhost',
    'hook-port' : '666',
    'hook-passwd' : 'passwd',
    'hook-projects' : "[ 'master' ]",
    'hook-script' : './gitpoller_hook_script.sh',
    'hook-user' : 'test_user',
    'description' : "Exercise the GitPollerService",
}

# configure python logging level from config dict
numeric_level = getattr(plog, config_dict['log-level'], None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(config_dict['log-level']))
plog.basicConfig(level = numeric_level)

# build up the poller factory and the poller service
step = int(config_dict['poll-interval'])
bbhook_factory = BuildbotHookFactory()
poller_factory = GitPollerFactory()
service_factory = GitPollerServiceFactory(hook_factory = bbhook_factory,
                                          poller_factory = poller_factory)
service = service_factory.make_service(config_dict = config_dict)

# set service parent to the magic 'application' variable
application = Application(config_dict['description'])
service.setServiceParent(application)

plog.info("Created BuildbotHookFactory with id: {0}".format(id(bbhook_factory)))
plog.info("Created GitPollerFactory with id: {0}".format(id(poller_factory)))
plog.info("Created GitPollerServiceFactory with id: {0}".format(id(service_factory)))
plog.info("GitPollerServiceFactory made GitPollerService with id: {0}".format(id(service)))
plog.info("Created Application object with id: {0}".format(id(application)))
