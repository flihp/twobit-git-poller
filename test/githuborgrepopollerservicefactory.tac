#!/usr/bin/env python

import logging, os

from twisted.application.service import Application
from twisted.python import log as tlog

from twobit.gitutil import GitHubOrgRepoPollerFactory
from twobit.twisted_gitpoller import GitHubOrgRepoPollerServiceFactory

""" Test TAC file / program to exercise the GitPollerService
"""

# configuration for the GitPollerService
config_dict = {
    'basedir' : os.getcwd(),
    'log-level' : 'DEBUG',
    'name' : 'openxt',
    'poll-interval' : '300',
    'hook-logfile' : './hook.log',
    'hook-master' : 'localhost',
    'hook-port' : '666',
    'hook-passwd' : 'passwd',
    'hook-projects' : "[ 'master' ]",
    'hook-script' : './gitpoller_hook_script.sh',
    'hook-user' : 'test_user',
    'description' : "Exercise the GitPollerService",
}

def mycallback(remote=None, org=None):
    """ Invoked for each repo the GitHubOrgRepoPoller finds in the provided
        org.
    """
    log = logging.getLogger(__name__)
    log.info("callback got remote: {0} from github org: {1}"
             .format(remote, org._orgname))

# convert 'log-level' string from config_dict to numeric value from python
#   logging
numeric_level = getattr(logging, config_dict['log-level'], None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(config_dict['log-level']))
# configure python logging to use the provided log level
#   and the same log stream as the twisted framework
stream_handler = logging.StreamHandler(stream = tlog.logfile)
logging.basicConfig(level = numeric_level, stream = stream_handler.stream)

# build up the poller factory and the poller service
poller_factory = GitHubOrgRepoPollerFactory()
service_factory = GitHubOrgRepoPollerServiceFactory(poller_factory = poller_factory)
service = service_factory.make_service(config_dict = config_dict,
                                       callback = mycallback)
# set service parent to the magic 'application' variable
application = Application(config_dict['description'])
service.setServiceParent(application)
