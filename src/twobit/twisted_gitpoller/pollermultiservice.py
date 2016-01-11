from ConfigParser import SafeConfigParser
import logging
# from exception import RuntimeError, FileNotFoundError
from twisted.application.service import ServiceMaker, MultiService
from twisted.python import log
from twisted.python.usage import Options
from twobit.buildbotutil import BuildbotHookFactory
from twobit.gitutil import GitPollerFactory, GitHubOrgRepoPollerFactory
from twobit.twisted_gitpoller import GitPollerServiceFactory, GitHubOrgRepoPollerServiceFactory

import logging

class PollerMultiServiceFactoryOptions(Options):
    optParameters = [
        ['log-level', 'l', 'WARNING', 'python logging level'],
        ['config', 'c', 'config.ini',
         "Configuration file describing the configuration of some number of pollers"]
    ]

class PollerMultiServiceFactory(ServiceMaker):
    """ A factory class that makes PollerMultiService instances.

    The primary function of this class is to parse the configuration file
    specified and create the proper poller for the given value of the
    'type' option.
    Currently it only supports the 'git' type, using a
    GitPollerServiceFactory to create a GitPollerService to poll the
    specified git repo.
    """
    tapname = "twobit_poller"
    description = "Poll stuff."
    options = PollerMultiServiceFactoryOptions

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def makeService(self, options={}):
        """ Make and configure PollerMultiService

        The configuration of the PollerMultiService is determined by the
        configuration file specified in the option dictionary under the key
        'config'.
        """
        numeric_level = getattr(logging, options['log-level'].upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("Invalid log level: {0}".format(config_dict['log-level']))
        stream_handler = logging.StreamHandler(stream = log.logfile)
        logging.basicConfig(level = numeric_level, stream = stream_handler.stream)

        self._log.debug('make_service')
        config = SafeConfigParser()
        config.read(options['config'])
        # build up factory objects needed to make GitPollerSerice
        hook_factory = BuildbotHookFactory()
        gp_factory = GitPollerFactory()
        gps_factory = GitPollerServiceFactory(hook_factory = hook_factory,
                                              poller_factory = gp_factory)
        # build up factory objects needed to make GitHubOrgRepoPollerService
        ghorp_factory = GitHubOrgRepoPollerFactory()
        ghorps_factory = GitHubOrgRepoPollerServiceFactory(poller_factory = ghorp_factory)
        pms = PollerMultiService(service_factory = gps_factory)
        for section in config.sections():
            self._log.info("processing config section: {0}".format(section))
            config_dict = dict(config.items(section))
            if 'type' not in config_dict:
                raise ValueError("Missing required option 'type' from "
                                 "config section {0}".format(section))
            elif config_dict['type'] == 'git':
                self._log.info("creating GitPollerService for option 'type' "
                               "with value 'git'")
                service = gps_factory.make_service(config_dict = config_dict)
            elif config_dict['type'] == 'org':
                self._log.info("creating GitRepoPoller")
                service = ghorps_factory.make_service(config_dict = config_dict,
                                                      callback = pms.add_repo_from_org)

            else:
                raise NotImplementedError("Config section {0} specifies an "
                    "unknown value for the option 'type': {1}".format(section,
                        config_dict['type']))
            pms.addService(service)
        return pms

class PollerMultiService(MultiService):
    """ A collection of GitPollerService and GitHubPollerService objects.

    This class creates a collection of GitPollerSerivce and
    GitHubPollerService objects from the provided config file. They are then
    made children of this top level object.
    """
    def __init__(self, service_factory=None, config=None):
        """ Initialize an instance of the PollerMultiService.

        service_factory: A GitPollerServiceFactory for creating new
        GitPollerServices on demand. This is used when a
        GitHubOrgRepoPollerService emits a repo URL that we don't yet have
        a poller service running for.
        """
        MultiService.__init__(self)
        self._log = logging.getLogger()
        self._log.info('PollerMultiService __init__')
        self._config = config
        self._service_factory = service_factory

    def add_repo_from_org(self, org=None, remote=None, data={}):
        """ Add a new GitRepoPollerService to the multi service.

        This method is intended to be used as a callback by a
        GitHubOrgRepoPoller. Each time the Org is polled this method
        should be invoked for each repo discovered. If the multi service
        doesnt already have a GitRepoPollerService for the given repo it
        will create one and make it a child.
        """
        if org is None:
            raise ValueError('add_repo_from_org received invalid org: {0}'
                             .format(org))
        if remote is None:
            raise ValueError('add_repo_from_org received invalid remote: {0}'
                             .format(remote))
        self._log.debug("add_repo_from_org with remote: {0}".format(remote))
        try:
            service = self.getServiceNamed(remote)
            self._log.info("Named service {0} already exists in "
                           "PollerMultiService: {1}".format(remote, id(self)))
            return
        except KeyError as keyerr:
            """ No service with this name, make a new one.
            """
            self._log.info("No service named {0}, creating a new one")
            service = self._service_factory.make_service(config_dict = data)
            self.addService(service)
