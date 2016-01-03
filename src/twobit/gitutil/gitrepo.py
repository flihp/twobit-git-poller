import logging, subprocess

class GitError(Exception):
    def __init__(self, message):
        super(GitError, self).__init__(message)

class GitRepo(object):
    """ Class wrapping a git repository.
    """
    def __init__(self, gitdir=None):
        self._log = logging.getLogger(__name__)
        self._log.debug("constructor")
        self._gitdir = gitdir

    def get_gitdir(self):
        return self._gitdir

    def get_branches(self):
        """ Get list of branch names for git repo """
        self._log.debug("get_branches")
        if self._gitdir is None:
            raise GitError("gitdir must be set to get branch names")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'branch']
        self._log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').replace('*', '').split()

    def get_symname(self, branch=None):
        """ Translate a branch name to a string holding the full symbolic name """
        if branch is None:
            raise GitError("branch name must be set to get symname")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'rev-parse',
               '--symbolic-full-name', branch]
        self._log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').strip()

    def get_hash(self, name):
        """ Get the object hash for a named object
        """
        self._log.debug("get_hash")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'rev-parse', name]
        self._log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').strip()

class GitMirror(object):
    """ Class used to maintain a mirror of a remote git repo
    """
    def __init__(self, remote=None, repo=None):
        """ Constructor

        remote: the URL for the remote repo to mirror
        mirror: path to the local mirror
        """
        self._log = logging.getLogger(__name__)
        self._log.debug('constructor')
        self._repo = repo
        self._remote = remote

    def get_remote(self):
        return self._remote

    def mirror(self):
        if self._remote is None:
            raise GitError("Mirror called without a repo set")
        if self._repo is None:
            raise GitError("Mirror called without a GitRepo object set")
        self._log.debug("Mirroring {0} at {1}."
                        .format(self._remote, self._repo.get_gitdir()))
        cmd = ['git', 'clone', '--mirror', self._remote,
               self._repo.get_gitdir()]
        self._log.info("Executing command: {0}".format(cmd))
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def update(self):
        """ Update an existing repo
        """
        if self._repo is None:
            raise GitError("Cannot update without a remote to update.")
        self._log.debug("Updating an existing mirror {0} from remote {1}."
                        .format(self._repo.get_gitdir(), self._remote))
        cmd = ['git', '--git-dir={0}'.format(self._repo.get_gitdir()),
               'remote', 'update']
        self._log.info("Executing command: {0}".format(cmd))
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
