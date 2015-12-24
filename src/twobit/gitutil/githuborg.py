import logging as log
import json
from urllib2 import urlopen

class GitHubOrg(object):
    """ GitHubOrg class

    Give this class the name of a github org. It provides some
    convenience functions that will operate on the organization
    using the GitHub API.
    """
    _GITHUB_REPO_URL = 'https://api.github.com/orgs/{0}/repos'
    def __init__(self, orgname=None):
        self._orgname = orgname
        self._url = self._GITHUB_REPO_URL.format(self._orgname)

    def get_repos(self):
        """ Poll all repos from a GitHub org.

        Returns an array of dictionaries representing the repos in the
        GitHub org.
        """
        repo_urls = []
        nexturl = self._url
        while nexturl is not None:
            github_req = urlopen(nexturl)
            for repo in json.load(github_req):
                log.debug("GitHubOrg repo: {0}".format(repo))
                repo_urls.append(repo['git_url'])
            headers = github_req.info()
            for link in headers['link'].split(','):
                link_elements = link.strip().split(';')
                if link_elements[-1].strip() == 'rel="next"':
                    nexturl = link_elements[0].strip(' \t\n\r<>')
                    log.debug("GitHubOrg nexturl: {0}"
                              .format(nexturl))
                    break
                else:
                    nexturl = None
        return repo_urls
