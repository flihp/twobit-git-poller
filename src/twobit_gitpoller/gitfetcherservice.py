from __future__ import print_function

from twisted.python import log
from twisted.application.internet import TimerService
from twisted.application.service import IService, IServiceCollection, MultiService
from zope.interface import implements

class GitFetcherService(TimerService):
    """ GitFetcherService

    Simple class that wraps a GitFetcher and the TimerService to poll on a
    git repo on an interval.
    """
    implements(IService)
    def __init__(self, fetcher=None, step=60*5):
        """ The magic here is calling the TimerService constructor (old
            style class) to set the polling interval and specify the polling
            function.
        """
        if fetcher is None:
            raise RuntimeError('fetcher cannot be None')
        self._fetcher = fetcher
        TimerService.__init__(self, step=step, callable=self._fetcher.poll)
