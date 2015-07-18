from __future__ import print_function

from twisted.python import log
from twisted.application.internet import TimerService
from twisted.application.service import IService, IServiceCollection, MultiService
from zope.interface import implements

class GitFetcherService(MultiService):
    """
    """
    implements(IService, IServiceCollection)

    def __init__(self, step=60*5):
        MultiService.__init__(self)
        self._step = step

    def add_fetcher(self, fetcher=None):
        if fetcher is None:
            raise RuntimeError('fetcher cannot be None')
        if self._fetcher is not None:
            raise RuntimeError('fetcher already populated')
        self._fetcher = fetcher
        self._timer = TimerService(step=self._step,
                                   callable=self._fetcher.poll)
        self.addService(self)
