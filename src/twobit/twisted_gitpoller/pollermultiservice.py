from ConfigParser import SafeConfigParser
import logging
# from exception import RuntimeError, FileNotFoundError
from twisted.application.service import ServiceMaker, MultiService
from twisted.python import log
from twisted.python.usage import Options
from twobit.buildbotutil import BuildbotHookFactory
from twobit.gitutil import GitPollerFactory
from twobit.twisted_gitpoller import GitPollerServiceFactory

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
        hook_factory = BuildbotHookFactory()
        poller_factory = GitPollerFactory()
        gps_factory = GitPollerServiceFactory(hook_factory = hook_factory,
                                              poller_factory = poller_factory)
        pms = PollerMultiService()
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
                pms.addService(service)
            else:
                raise NotImplementedError("Config section {0} specifies an "
                    "unknown value for the option 'type': {1}".format(section,
                        config_dict['type']))
        return pms

class PollerMultiService(MultiService):
    """ A collection of GitPollerService and GitHubPollerService objects.

    This class creates a collection of GitPollerSerivce and
    GitHubPollerService objects from the provided config file. They are then
    made children of this top level object.
    """
    def __init__(self):
        MultiService.__init__(self)
        self._log = logging.getLogger()
        self._log.info('PollerMultiService __init__')
