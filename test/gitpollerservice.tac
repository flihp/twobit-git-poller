#!/usr/bin/env python

from argparse import ArgumentParser
import logging as plog
import ast, os

from twisted.application.service import Application
from twisted.python import log as tlog

from twobit.gitutil import GitPollerFactory
from twobit_gitpoller import GitPollerService

""" Test TAC file / program to exercise the GitPollerService
"""

# configuration for the GitPollerService
config_dict = {
    'basedir' : os.getcwd(),
    'gitdir' : 'mirror.git',
    'url' : 'remote.git',
    'log-level' : 'INFO',
    'poll-interval' : '30',
    'description' : "Exercise the GitPollerService",
}

# configure python logging level from config dict
numeric_level = getattr(plog, config_dict['log-level'], None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(config_dict['log-level']))
plog.basicConfig(level = numeric_level)

# build up the poller factory and the poller service
step = int(config_dict['poll-interval'])
factory = GitPollerFactory()
poller = factory.make_poller(config_dict = config_dict)
service = GitPollerService(poller = poller, step = step)
# set service parent to the magic 'application' variable
application = Application(config_dict['description'])
service.setServiceParent(application)

plog.info("Created GitPollerFactory with id: {0}".format(id(factory)))
plog.info("GitPollerFactory made GitPoller with id: {0}".format(id(poller)))
plog.info("Created GitPollerService with id: {0}".format(id(service)))
plog.info("Created Application object with id: {0}".format(id(application)))
