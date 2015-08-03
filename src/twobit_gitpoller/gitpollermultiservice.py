import ast, os, sys

from ConfigParser import ConfigParser
# from exception import RuntimeError, FileNotFoundError
from twisted.application.internet import TimerService
from twisted.application.service import IService, IServiceCollection, MultiService
from twisted.python import log
from twobit_gitpoller import GitPoller, GitHubOrgFetcher, GitPollerService, GitPollerServiceFactory
from zope.interface import implements

class GitPollerMultiService(object, MultiService):
    implements(IService, IServiceCollection)
    """ A collection of GitPollerService and GitHubPollerService objects.

    This class creates a collection of GitPollerSerivce and
    GitHubPollerService objects from the provided config file. They are then
    made children of this top level object.
    """
    def __init__(self, service_factory=GitPollerServiceFactory()):
        MultiService.__init__(self)
        print('TwobitGitPoller __init__')
        self._service_factory = service_factory

    def add_config(self, conf_file=None):
        log.msg('TwobitGitPoller.add_config')
        if conf_file is None:
            raise RuntimeError('No config file provieded')
        if not os.path.isfile(conf_file):
            raise IOError("Config file doesn't exist: {0}".format(conf_file))
        # get application config values
        self._config = ConfigParser()
        self._config.read(conf_file)
        self._logdir = self._config.get('DEFAULT', 'logdir')
        self._logfile = self._config.get('DEFAULT', 'logfile')
        # conservative default polling interval
        self._poll_interval_default = 1200

    def load_config(self):
        """ load_config(self):
        """
        log.msg('TwobitGitPoller.load__config')
        if self._config is None:
            raise RuntimeError('No config provided')
        # clean out any existing service objects
        for service in self:
            self.removeService(service)
        # Iterate over repos from config file
        for section in self._config.sections():
            # Get config values, use defaults if necessary.
            config_dict = dict(self._config.items(section))
            services = self._service_factory.make_services(config_dict)
            for service in services:
                self.addService(service)
