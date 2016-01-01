import logging as log
import os
from twobit.gitutil import GitRepo, GitMirror, GitPoller

class GitPollerFactoryValueError(ValueError):
    """ An exception class derived from ValueError.
    
    This class is used to report errors and omissions in the values
    passed to the GitPollerFactory.
    """
    def __init__(self, message):
        super(GitPollerFactoryValueError, self).__init__("Missing "
            "required value in config dictionary: {0}".format(message))

class GitPollerFactory(object):
    """ A factory that builds GitPoller objects from a Bitbake hook object
        and a configuration dictionary.

    """
    def __init__(self, hook_factory=None):
        """ Initialize the GitPollerFactory

        The parameter hook_factory is a factory for creating hook objects.
        """
        self._hook_factory = hook_factory

    def make_poller(self, config_dict=None, hook=None):
        """ Create a GitPoller from the provided configuration data.

        The nature of the GitPoller and the TimerService is determined by the
        values in the config_dict parameter. These are:
        basedir: directory where url will be cloned
        url: URL of git remote
        hook: hook object to execute when poller is updated
        """
        if config_dict is None:
            raise ValueError('config_dict cannot be None')
        if not 'basedir' in config_dict:
            raise GitPollerFactoryValueError("basedir")
        if not 'url' in config_dict:
            raise GitPollerFactoryValueError("url")
        if hook is not None:
            log.info("GitPollerFactory using hook object provided to "
                     "make_poller")
            use_hook = hook
        elif self._hook_factory is not None:
            log.info("GitPollerFactory using hook factory provided to "
                     "constructor")
            use_hook = self._hook_factory.make_buildbothook(config_dict)
        else:
            log.info("GitPollerFactory creating GitPoller with no hook")
            use_hook = None
        """ build up 
        if gitdir is relative, it's relative to basedir
        if gitdir is absolute, basedir is ignored
        """
        if os.path.isabs(config_dict['gitdir']):
            gitdir = config_dict['gitdir']
        else:
            gitdir = os.path.join(config_dict['basedir'], config_dict['gitdir'])
        repo = GitRepo(gitdir = gitdir)
        mirror = GitMirror(remote = config_dict['url'], repo = repo)
        return GitPoller(hook = use_hook, mirror = mirror, repo = repo)
