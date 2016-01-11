#!/usr/bin/env python

import logging as plog

from twisted.application.service import Application
from twisted.python import log as tlog

from twobit.buildbotutil import BuildbotHookFactory
from twobit.gitutil import GitPollerFactory
from twobit.twisted_gitpoller import PollerMultiServiceFactory

""" Test TAC file / program to exercise the PollerMultiServiceFActory
"""
config_dict = {
    'config' : { 'config' : 'pollermultiservice.ini',
                 'log-level' : 'WARNING' },
    'description' : "test program to test plugging the "
        "PollerMultiServiceFactory into the twisted event loop manually",
    'log_level' : 'DEBUG'
}
# convert 'log-level' string from config_dict to numeric value from python
#   logging
numeric_level = getattr(plog, config_dict['log_level'].upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(config_dict['log_level']))
# configure python logging to use the provided log level
#   and the same log stream as the twisted framework
stream_handler = plog.StreamHandler(stream = tlog.logfile)
plog.basicConfig(level = numeric_level, stream = stream_handler.stream)

pmsf = PollerMultiServiceFactory()
pms = pmsf.makeService(options=config_dict['config'])

# set service parent to the magic 'application' variable
application = Application(config_dict['description'])
pms.setServiceParent(application)
