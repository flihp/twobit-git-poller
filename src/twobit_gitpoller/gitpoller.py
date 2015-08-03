from __future__ import print_function
import os, subprocess
from twisted.python import log
from twobit_gitpoller import IPoll

class GitPoller(IPoll):
    """ GitPoller class

    Give this class a URL for a git repo and it will fetch it for you.
    """

    def __init__(self, repo_url = None, basedir = '/tmp', hook=None):
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
            print('git --git-dir={0} branch'.format(self.repo_path))
            return subprocess.check_output(
                       ['git', '--git-dir=' + self.repo_path, 'branch']
                   ).decode('utf-8').replace('*', '').split()
        except subprocess.CalledProcessError, e:
            print(e)
            return []

    def _get_symname(self, branch):
        """ Translate a branch name to a string holding full symbolic name
        """
        try:
            print('git --git-dir={0} rev-parse --symbolic-full-name {1}'.format(self.repo_path, branch))
            return subprocess.check_output(
                       ['git', '--git-dir=' + self.repo_path, 'rev-parse',
                        '--symbolic-full-name', branch]
                   ).decode('utf-8').strip()
        except subprocess.CalledProcessError, e:
            print(e)
            return None

    def _get_hash(self, name):
        """ Get the object hash for named object as string
        """
        try:
            print('git --git-dir={0} rev-parse {1}'.format(self.repo_path, name))
            return subprocess.check_output(
                       ['git', '--git-dir=' + self.repo_path, 'rev-parse',
                        name]
                   ).decode('utf-8').strip()
        except subprocess.CalledProcessError, e:
            print(e)
            return None

    def poll(self):
        """ Poll a git repo.

        Each call to the 'poll' method will do exactly what you expect:
        the repository will be polled and updated. If the repo exists
        locally it's fetched, otherwised a bare clone is made.
        """
        # sanity check config and directory structure
        print('polling for repo ' + self.repo_name);
        if self.repo_url is None:
            print('GitPoller: no repo url set, nothing to poll.')
            return
        if not os.path.lexists(self.basedir):
            os.mkdir(self.basedir)
        elif not os.path.isdir(self.basedir):
            print('GitPoller: {0} exists but is not a directory. Aborting'.format(self.basedir))
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
                    print('branch is None or empty')
                    break
                symname = self._get_symname(branch)
                if symname is None or not symname:
                    print('symname for branch "{0}" is None or empty'.format(branch))
                    break
                hook_data.append((symname, self._get_hash(symname)))
        print('for repo {0} at URL {1}: '.format(self.repo_name, self.repo_url), end='')
        try:
            if not os.path.exists(self.repo_path):
                print('cloning mirror into {0}'.format(self.repo_path))
                subprocess.check_output(
                    ['git', 'clone', '--mirror', self.repo_url, self.repo_path],
                    stderr=subprocess.STDOUT
                    )
            elif os.path.isdir(self.repo_path):
                print('updating existing mirror')
                subprocess.check_output(
                    ['git', '--git-dir=' + self.repo_path, 'remote', 'update'],
                    stderr=subprocess.STDOUT
                )
            else:
               print('{0} exists but is not a directory, bad news'.format(self.repo_path))
            print('success polling repo: {0}'.format(self.repo_url))
        except subprocess.CalledProcessError, e:
           print('{0}'.format(e))
        if (self.hook is not None and
            self.hook.script is not None and
            len(hook_data) > 0):
            # Invoke hook script for each project string, can only pass one
            # at a time (I think).
            for project in self.hook.projects:
                try:
                    p = subprocess.Popen(
                            [self.hook.script,
                             '--master={0}:{1}'.format(self.hook.host,
                                                       self.hook.port),
                             '--username=' + self.hook.user,
                             '--auth=' + self.hook.passwd,
                             '--logfile=' + self.hook.logfile,
                             '--verbose', '--verbose', '--verbose',
                             '--project=' + project
                            ],
                            env={'GIT_DIR' : self.repo_path},
                            stdin=subprocess.PIPE
                        )
                    for hook_set in hook_data:
                        post = self._get_hash(hook_set[0])
                        if post is None or not post:
                            print(' post object hash is None or empty')
                            break
                        p.stdin.write(
                            '{0} {1} {2}\n'.format(hook_set[1], post, hook_set[0])
                        )
                    p.stdin.close()
                except OSError, e:
                    log.msg('Failed to execute hook script: {0}'.format(e))
