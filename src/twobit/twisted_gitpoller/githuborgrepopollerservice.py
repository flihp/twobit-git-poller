import logging
from twisted.application.internet import TimerService
from twobit.gitutil import IPoll

class GitHubOrgRepoPollerService(TimerService):
    """ This looks a lot like the other poller service ...

    Probably best to use the TimerService directly.
    """
    def __init__(self, poller=None, step=300):
        """
        """
        if poller is None:
            raise RuntimeError('poller cannot be None')
        if not issubclass(type(poller), IPoll):
            raise TypeError('poller privided is not a subclass of IPoll')
        self._poller = poller
        TimerService.__init__(self, step=step, callable=self._poller.poll)

class GitHubOrgRepoPollerServiceFactory(object):
    """
    """
    def __init__(self, poller_factory=None):
        """
        poller_factory is a GitHubOrgRepoPollerFactory. We use it to create
        GitHubOrgRepoPoller ojbects that we attach to the
        GitHubOrgRepoPollerService instances that this factory creates.
        """
        self._log = logging.getLogger(__name__)
        self._poller_factory = poller_factory

    def make_service(self, poller=None, config_dict={}, callback=None):
        if 'poll-interval' in config_dict:
            step = int(config_dict['poll-interval'])
        else:
            step = 300
        if self._poller_factory is None:
            raise ValueError('No poller factory privided.')
        poller = self._poller_factory.make_poller(config_dict = config_dict,
                                                  callback = callback)
        self._log.info("Creating GitHubOrgRepoPollerService for "
                       "GitHubOrgRepoPoller: {0}".format(poller))
        service = GitHubOrgRepoPollerService(poller = poller, step = step)
        service.setName(poller.get_org().get_name())
        return service
