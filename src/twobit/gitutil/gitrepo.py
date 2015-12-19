import subprocess
import logging as log

class GitError(Exception):
    def __init__(self, message):
        super(GitError, self).__init__(message)

class GitRepo(object):
    """ Class wrapping a git repository.
    """
    def __init__(self, gitdir=None):
        log.debug("GitRepo constructor")
        self._gitdir = gitdir

    def get_branches(self):
        """ Get list of branch names for git repo """
        log.debug("get_branches")
        if self._gitdir is None:
            raise GitError("gitdir must be set to get branch names")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'branch']
        log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').replace('*', '').split()

    def get_symname(self, branch=None):
        """ Translate a branch name to a string holding the full symbolic name """
        if branch is None:
            raise GitError("branch name must be set to get symname")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'rev-parse',
               '--symbolic-full-name', branch]
        log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').strip()

    def get_hash(self, name):
        """ Get the object hash for a named object
        """
        log.debug("get_hash")
        cmd = ['git', '--git-dir={0}'.format(self._gitdir), 'rev-parse', name]
        log.info("executing cmd: {0}".format(cmd))
        return subprocess.check_output(cmd).decode('utf-8').strip()

class GitMirror(object):
    """ Class used to maintain a mirror of a remote git repo
    """
    def __init__(self, remote, mirror):
        """ Constructor

        remote: the URL for the remote repo to mirror
        mirror: path to the local mirror
        """
        log.debug("GitMirror init")
        self._remote = remote
        self._mirror = mirror

    def mirror(self):
        if self._remote is None:
            raise GitError("Mirror called without remote set")
        if self._mirror is None:
            raise GitError("Mirror called without gitdir set")
        log.debug("Mirroring {0} at {1}.".format(self._remote, self._mirror))
        cmd = ['git', 'clone', '--mirror', self._remote, self._mirror]
        log.info("Executing command: {0}".format(cmd))
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def update(self):
        """ Update an existing repo
        """
        log.debug("Updating an existing mirror {0} from remote {1}."
                  .format(self._mirror, self._remote))
        if self._mirror is None:
            raise GitError("Cannot update without gitdir set.")
        cmd = ['git', '--git-dir={0}'.format(self._mirror), 'remote',
               'update']
        log.info("Executing command: {0}".format(cmd))
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
