from __future__ import print_function

import os, subprocess, sys
from json import load
from twisted.application.service import IServiceCollection, MultiService
from twobit_gitpoller import GitPoller, GitPollerService, IPoll
from urllib2 import urlopen, URLError
from zope.interface import implements

class GitHubOrgPoller(MultiService, IPoll):
    """ Fetch and poll all repos from a GitHub org.

    Poll github org finding each repo in the org.  For each repo we
    create a GitPoller if one doesn't already exit and we create a
    TimeService and hook it up to the supplied application object.
    """
    implements(IServiceCollection)
    _GITHUB_REPO_URL = 'https://api.github.com/orgs/{0}/repos'
    def __init__(self, orgname, destdir, poll_interval=300, hook=None):
        MultiService.__init__(self)
        self._destdir = destdir
        self._pollers = {}
        self._orgname = orgname
        self._poll_interval = poll_interval
        self._hook = hook
        self._url = self._GITHUB_REPO_URL.format(self._orgname)

    def poll(self):
        """ Poll all repos from a GitHub org.

        This function operates on data from the constructior.  First
        data about each repo from the specified GitHub org is retrieved
        via the GitHub API. Then a GitPoller is created for each repo.
        A twisted TimeService with the appropriate poll interval is
        then created for each repo from the org.  Upon subsequent
        invocations new GitPollers are created for new repos.

        See: https://developer.github.com/v3/repos/
        """
        nexturl = self._url
        while nexturl != '':
            print('GitHubOrgPoller: opening URL: {0}'.format(nexturl))
            try:
                github_req = urlopen(nexturl)
            except URLError as err:
                print('GitHubOrgPoller: URLError: {0}'.format(err))
                break

            # Get repos from the JSON body of the request.  If a
            # GitPoller for this repo doesn't already exist create
            # one.
            for repo in load(github_req):
                if not repo['git_url'] in self._pollers:
                    print('GitHubOrgPoller: Creating poller for repo: {0}'.format(repo['git_url']))
                    poller = self._poller_from_github(repo)
                    self._pollers[repo['git_url']] = poller
                    service = GitPollerService(poller,
                                               step=self._poll_interval)
                    self.addService(service)
                else:
                    print('GitHubOrgPoller: poller for repo {0} already exists'.format(repo['git_url']))

            # Find the 'next' link from the link header (if it exists).
            # If no 'next' link exists we're at the end of the Org's
            # repos.
            headers = github_req.info()
            for link in headers['link'].split(','):
                link_elements = link.strip().split(';')
                if link_elements[-1].strip() == 'rel="next"':
                    nexturl = link_elements[0].strip(' \t\n\r<>')
                    break
                else:
                    nexturl = ''

    def _poller_from_github(self, repo):
        """ Create GitPoller from GitHub repo dictionary.
        """
        if not 'git_url' in repo:
            sys.exit('Github repo has no git_url?')
        if not os.path.lexists(self._destdir):
            os.makedirs(self._destdir)
        elif not os.path.isdir(self._destdir):
            sys.exit('Required directory {0} for github repo {1} exists but is not a directory.\n'.format(self._destdir, repo['name']))
        print('Creating GitPoller for {0} in {1}\n'.format(repo['git_url'], self._destdir))
        return GitPoller(repo['git_url'], basedir=self._destdir, hook=self._hook)
