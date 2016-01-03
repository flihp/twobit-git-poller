import json, logging
from urllib2 import urlopen

class GitHubOrg(object):
    """ GitHubOrg class

    Give this class the name of a github org. It provides some
    convenience functions that will operate on the organization
    using the GitHub API.
    """
    _GITHUB_REPO_URL = 'https://api.github.com/orgs/{0}/repos'
    def __init__(self, orgname=None):
        self._log = logging.getLogger(__name__)
        self._orgname = orgname
        self._url = self._GITHUB_REPO_URL.format(self._orgname)

    def get_repo_git_urls(self):
        """ Get URLs for all git repos in an organization.

        Returns an array of URL strings.
        """
        self._log.debug("GitHubOrg.get_repo_urls() called")
        repo_urls = []
        for repo in self.get_repos():
            self._log.debug("GitHubOrg repo: {0}".format(repo))
            repo_urls.append(repo['git_url'])
        return repo_urls

    def get_repos(self):
        """ Poll all repos from a GitHub org.

        Returns an array of dictionaries representing the repos in the
        GitHub org.
        """
        self._log.debug("GitHubOrg.get_repos() called")
        org_repos = []
        nexturl = self._url
        while nexturl is not None:
            self._log.info("requesting url: {0}".format(nexturl))
            github_req = urlopen(nexturl)
            req_data = json.load(github_req)
            self._log.debug("appending repo data: {0}".format(req_data))
            org_repos.extend(req_data)
            headers = github_req.info()
            for link in headers['link'].split(','):
                link_elements = link.strip().split(';')
                if link_elements[-1].strip() == 'rel="next"':
                    nexturl = link_elements[0].strip(' \t\n\r<>')
                    self._log.debug("GitHubOrg nexturl: {0}".format(nexturl))
                    break
                else:
                    nexturl = None
        return org_repos
