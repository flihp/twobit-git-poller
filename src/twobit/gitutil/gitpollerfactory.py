import logging as log
import os
from twobit.gitutil import GitRepo, GitMirror, GitPoller

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
            raise ValueError("Required config item missing from org: basedir")
        if not 'url' in config_dict:
            raise ValueError("Required section missing from git section: url")
        if hook is not None:
            log.info("GitPollerFactory using hook object provided to "
                     "make_poller")
            use_hook = hook
        elif self._hook_factory is not None:
            log.info("GitPollerFactory using hook factory provided to "
                     "constructor")
            use_hook = self._hook_factory(config_dict)
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
        return GitPoller(mirror = mirror, repo = repo)
