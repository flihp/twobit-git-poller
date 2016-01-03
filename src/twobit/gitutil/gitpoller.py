from __future__ import print_function
import logging, os, subprocess
from twobit_gitpoller import IPoll
from twobit.gitutil import GitMirror, GitRepo

class GitPoller(IPoll):
    """ GitPoller class

    Give this class a URL for a git repo and it will fetch it for you.
    """

    def __init__(self, mirror=None, repo=None, hook=None):
        """ Initialize the GitPoller object.

        basedir: The directory under which the gitrepo will be cloned.
        mirror:  An instance of the twobit.gitutil.GitMirror object.
        repo:    An instance of the twobit.gitutil.GitRepo object.
        hook:    An instance of the twobit_gitpoller.BuildbotHook object.
        """
        self._log = logging.getLogger(__name__)
        self._hook = hook
        self._mirror = mirror
        self._repo = repo
        self._gitdir = self._repo.get_gitdir()
        self._log.debug("GitPoller constructor: hook={0}, mirror={1}, "
                        "repo={2}, gitdir={3}".format(id(hook), id(mirror),
                                                      id(repo), self._gitdir))

    def poll(self):
        """ Poll a git repo.

        Each call to the 'poll' method will do exactly what you expect:
        the repository will be polled and updated. If the repo exists
        locally it's fetched, otherwised a bare clone is made.
        """
        # sanity check config and directory structure
        self._log.info("poller {0} polling on mirror {1}"
                       .format(id(self), id(self._mirror)));
        if (os.path.lexists(self._gitdir) and
            not os.path.isdir(self._gitdir)):
            self._log.error('GitPoller: {0} exists but is not a directory. Aborting'
                            .format(self._gitdir))
        # if the gitdir doesn't exist yet we need to make a fresh mirror
        # in this case we skip the buildbot hook script
        if not os.path.exists(self._gitdir):
            self._log.info("Mirroring GitRepo {0} with GitMirror {1} at {2}"
                           .format(self._repo, self._mirror, self._gitdir))
            self._mirror.mirror()
            return
        # Get hook data for each branch in the repo before we update the gitdir
        hook_data = []
        for branch in self._repo.get_branches():
            # for each branch create tuple of (symname, hash)
            # & add to list
            if branch is None or not branch:
                self._log.warning('branch is None or empty')
                continue
            symname = self._repo.get_symname(branch)
            if symname is None or not symname:
                self._log.warning('symname for branch "{0}" is None or empty'
                                  .format(branch))
                break
            sym_hash = self._repo.get_hash(symname)
            self._log.debug("symname: {0} with hash: {1}"
                            .format(symname, sym_hash))
            hook_data.append((symname, sym_hash))
        try:
            if os.path.isdir(self._gitdir):
                self._log.debug('updating existing mirror')
                self._mirror.update()
            else:
               self._log.error("{0} exists but is not a directory, bad news"
                               .format(self._gitdir))
            self._log.debug('success polling repo: {0} by object {1}'
                            .format(self._mirror.get_remote(), id(self)))
        except subprocess.CalledProcessError as excep:
           self._log.critical(excep)
        if self._hook is None:
            self._log.info("No hook object, skipping")
            return
        # execute the hook script for each branch
        for hook_set in hook_data:
            new_hash = self._repo.get_hash(hook_set[0])
            self._hook.exec_hook(data=(hook_set[0], hook_set[1], new_hash), gitdir=self._gitdir)
