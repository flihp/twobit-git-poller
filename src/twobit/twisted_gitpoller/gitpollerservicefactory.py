import logging

from twobit.buildbotutil import BuildbotHookFactory
from twobit.twisted_gitpoller import GitPollerService

class GitPollerServiceFactoryValueError(ValueError):
    def __init__(self, message):
        super(GitPollerServiceFactoryValueError, self).__init__("Missing "
              "required value in config dictionary: {0}".format(message))

class GitPollerServiceFactory(object):
    """
    """
    def __init__(self, hook_factory=None, poller_factory=None):
        self._log = logging.getLogger(__name__)
        self._hook_factory = hook_factory
        self._poller_factory = poller_factory

    def make_service(self, config_dict={}):
        if self._poller_factory is None:
            raise ValueError("GitPollerServiceFactory requires a "
                             "GitPollerFactory")
        if 'poll-interval' not in config_dict:
            raise GitPollerServiceFactoryValueError('poll-interval')
        step = int(config_dict['poll-interval'])
        if self._hook_factory is not None:
            hook = self._hook_factory.make_buildbothook(config_dict)
        else:
            hook = None
        poller = self._poller_factory.make_poller(config_dict = config_dict,
                                                  hook = hook)
        self._log.info('Creating GitPollerService for poller {0}'
                       .format(type(poller).__name__))
        return GitPollerService(poller = poller, step = step)