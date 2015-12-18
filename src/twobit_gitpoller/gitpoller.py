from __future__ import print_function
import os, subprocess
import logging as log
from twobit_gitpoller import IPoll

class GitPoller(IPoll):
    """ GitPoller class

    Give this class a URL for a git repo and it will fetch it for you.
    """

    def __init__(self, repo_url = None, basedir = '/tmp', hook=None):
        log.debug("GitPoller constructor: repo_url={0}, basedir={1}, hook={2}"
                  .format(repo_url, basedir, hook))
        self.repo_url = repo_url
        self.basedir = basedir
        self.repo_name = self.repo_url.split('/')[-1]
        self.repo_path = self.basedir + '/' + self.repo_name
        self.hook = hook
        # cloning bare repos adds '.git' to end of directory name even if URI
        # doesn't have one
        if self.repo_path[-4:] != '.git':
            self.repo_path = self.repo_path + '.git'

    def _get_branches(self):
        """ Get list of strings representing branches for git repo
        """
        try:
            cmd = ['git', '--git-dir={0}'.format(self.repo_path), 'branch']
            log.info('executing cmd: {0}'.format(cmd))
            return subprocess.check_output(cmd).decode('utf-8').replace('*', '').split()
        except subprocess.CalledProcessError as excep:
            log.critical(excep)
            return []

    def _get_symname(self, branch):
        """ Translate a branch name to a string holding full symbolic name
        """
        try:
            cmd = ['git', '--git-dir={0}'.format(self.repo_path), 'rev-parse',
                   '--symbolic-full-name={0}'.format(branch)]
            log.info('executing cmd: {0}'.format(cmd))
            return subprocess.check_output(cmd).decode('utf-8').strip()
        except subprocess.CalledProcessError as excep:
            log.critical(excep)
            return None

    def _get_hash(self, name):
        """ Get the object hash for named object as string
        """
        try:
            cmd = ['git', '--git-dir={0}'.format(self.repo_path), 'rev-parse', name]
            log.info('executing cmd: {0}'.format(cmd))
            return subprocess.check_output(cmd).decode('utf-8').strip()
        except subprocess.CalledProcessError as excep:
            log.critical(excep)
            return None

    def poll(self):
        """ Poll a git repo.

        Each call to the 'poll' method will do exactly what you expect:
        the repository will be polled and updated. If the repo exists
        locally it's fetched, otherwised a bare clone is made.
        """
        # sanity check config and directory structure
        log.info('poller {0} polling for repo {1}'
                 .format(id(self), self.repo_name));
        if self.repo_url is None:
            log.info('GitPoller: no repo url set, nothing to poll.')
            return
        if not os.path.lexists(self.basedir):
            os.mkdir(self.basedir)
        elif not os.path.isdir(self.basedir):
            log.error('GitPoller: {0} exists but is not a directory. Aborting'
                      .format(self.basedir))
        hook_data = []
        if (self.hook is not None and
            self.hook.script is not None and
            os.path.isdir(self.repo_path)):
            # Get hook data before remote update
            branches = self._get_branches()
            for branch in branches:
                # for each branch create tuple of (symname, hash)
                # & add to list
                if branch is None or not branch:
                    log.warning('branch is None or empty')
                    break
                symname = self._get_symname(branch)
                if symname is None or not symname:
                    log.warning('symname for branch "{0}" is None or empty'
                                    .format(branch))
                    break
                hook_data.append((symname, self._get_hash(symname)))
        log.info('for repo {0} at URL {1}: '
                 .format(self.repo_name, self.repo_url))
        try:
            if not os.path.exists(self.repo_path):
                log.info('cloning mirror into {0}'.format(self.repo_path))
                subprocess.check_output(
                    ['git', 'clone', '--mirror', self.repo_url, self.repo_path],
                    stderr=subprocess.STDOUT
                )
            elif os.path.isdir(self.repo_path):
                log.debug('updating existing mirror')
                cmd = ['git', '--git-dir={0}'.format(self.repo_path),
                       'remote', 'update']
                log.info('executing command: {0}'.format(cmd))
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            else:
               log.error('{0} exists but is not a directory, bad news'
                         .format(self.repo_path))
            log.debug('success polling repo: {0} by object {1}'
                      .format(self.repo_url, id(self)))
        except subprocess.CalledProcessError as excep:
           log.critical(excep)
        if (self.hook is not None and
            self.hook.script is not None and
            len(hook_data) > 0):
            # Invoke hook script for each project string, can only pass one
            # at a time (I think).
            for project in self.hook.projects:
                try:
                    cmd = [self.hook.script,
                           '--master={0}:{1}'.format(self.hook.host,
                                                     self.hook.port),
                           '--username=' + self.hook.user,
                           '--auth=' + self.hook.passwd,
                           '--logfile=' + self.hook.logfile,
                           '--verbose', '--verbose', '--verbose',
                           '--project=' + project]
                    env = {'GIT_DIR' : self.repo_path}
                    log.info('executing hook script: {0} with environment {1}'
                             .format(cmd, env))
                    p = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE)
                    for hook_set in hook_data:
                        post = self._get_hash(hook_set[0])
                        if post is None or not post:
                            log.warning(' post object hash is None or empty')
                            break
                        p.stdin.write('{0} {1} {2}\n'
                                      .format(hook_set[1], post, hook_set[0]))
                    p.stdin.close()
                except OSError as excep:
                    log.error('Failed to execute hook script: {0}'
                              .format(excep))
