from twisted.application.internet import TimerService
from twisted.application.service import IService
from zope.interface import implements

from twobit.gitutil import IPoll

class GitPollerService(TimerService):
    """ Periodically call the poll method of an IPoll object.

    Simple class that wraps a GitPoller and the TimerService to poll on a
    git repo on an interval.
    """
    implements(IService)
    def __init__(self, poller=None, step=60*5):
        """ The magic here is calling the TimerService constructor (old
            style class) to set the polling interval and specify the polling
            function.
        """
        if poller is None:
            raise RuntimeError('poller cannot be None')
        if not issubclass(type(poller), IPoll):
            raise TypeError('poller provided is not a subclass of IPoll');
        self._poller = poller
        TimerService.__init__(self, step=step, callable=self._poller.poll)
