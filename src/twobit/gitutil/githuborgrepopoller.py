import logging

class GitHubOrgRepoPoller(object):
    """ A class to poll a GitHub Organization for repositories.

    This class exposes a single method 'poll' that takes a callback
    as a parameter. Each time poll is called the GitHubOrg object is
    used to get the URL for each repository in the organization. The
    callback function passed to the function will be called for each
    repository URL in the GitHub organization.
    """
    def __init__(self, org=None, callback=None):
        self._log = logging.getLogger(__name__)
        self._org = org
        self._callback = callback

    def poll(self):
        """ Poll a GitHubOrg for repository urls.

        For each repo git url found we execute the provided callback. The
        callback function is expected to take 1 parameter:
        The URL of the git repository as a string.
        """
        for repo_git_url in self._org.get_repo_git_urls():
            self._log.info("Executing callback {0} for URL {1}"
                           .format(id(self._callback), repo_git_url))
            self._callback(repo_git_url)
