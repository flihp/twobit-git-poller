from copy import deepcopy
import logging
from twobit.gitutil import GitHubOrg, IPoll

class GitHubOrgRepoPoller(IPoll):
    """ A class to poll a GitHub Organization for repositories.

    This class exposes a single method 'poll' that takes a callback
    as a parameter. Each time poll is called the GitHubOrg object is
    used to get the URL for each repository in the organization. The
    callback function passed to the function will be called for each
    repository URL in the GitHub organization.
    """
    def __init__(self, org=None, callback=None, callback_data={}):
        self._log = logging.getLogger(__name__)
        self._org = org
        self._callback = callback
        self._callback_data = callback_data

    def get_org(self):
        return self._org

    def poll(self):
        """ Poll a GitHubOrg for repository urls.

        For each repo git url found we execute the provided callback. The
        callback function is expected to take 1 parameter:
        The URL of the git repository as a string.
        """
        for repo_git_url in self._org.get_repo_git_urls():
            self._log.info("Executing callback {0} for URL {1}"
                           .format(id(self._callback), repo_git_url))
            # add data about the repo to the data dictionary passed to the
            # callback
            if ('url' not in self._callback_data or
                'gitdir' not in self._callback_data):
                data = deepcopy(self._callback_data)
            else:
                data = self._callback_data
            if 'url' not in data:
                data['url'] = repo_git_url
            if 'gitdir' not in data:
                data['gitdir'] = repo_git_url.split('/')[-1]
                if data['gitdir'][-4:] != '.git':
                    data['gitdir'] = data['gitdir'] + '.git'
            self._callback(org = self._org, remote = repo_git_url, data = data)

class GitHubOrgRepoPollerFactory(object):
    """ Factory to create GitHubOrgRepoPollers from a configuration dictionary.
    """
    def __init__(self):
        self._log = logging.getLogger(__name__)

    def make_poller(self, config_dict={}, callback=None):
        """ Create a GitHubOrgPoller from the provided configuration dictionary.
        """
        if config_dict is None:
            raise ValueError("config_dict cannot be None")
        if not 'name' in config_dict:
            raise ValueError("config_dict must have 'name'.")
        org = GitHubOrg(config_dict['name'])
        return GitHubOrgRepoPoller(org = org, callback = callback, callback_data = config_dict)
