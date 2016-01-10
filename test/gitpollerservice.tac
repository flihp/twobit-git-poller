#!/usr/bin/env python

from argparse import ArgumentParser
import logging as plog
import ast, os

from twisted.application.service import Application
from twisted.python import log as tlog

from twobit.gitutil import GitPollerFactory
from twobit.twisted_gitpoller import GitPollerService

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

# convert 'log-level' string from config_dict to numeric value from python
#   logging
numeric_level = getattr(plog, config_dict['log-level'], None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(config_dict['log-level']))
# configure python logging to use the provided log level
#   and the same log stream as the twisted framework
stream_handler = plog.StreamHandler(stream = tlog.logfile)
plog.basicConfig(level = numeric_level, stream = stream_handler.stream)

log = plog.getLogger(__name__)

# build up the poller factory and the poller service
step = int(config_dict['poll-interval'])
factory = GitPollerFactory()
poller = factory.make_poller(config_dict = config_dict)
service = GitPollerService(poller = poller, step = step)
service.setName(poller.get_remote())
# set service parent to the magic 'application' variable
application = Application(config_dict['description'])
service.setServiceParent(application)
