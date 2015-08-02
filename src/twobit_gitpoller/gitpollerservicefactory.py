from twisted.python import log
from twobit_gitpoller import BuildbotHookFactory, GitFetcher, GitHubOrgFetcher, GitPollerService

class GitPollerServiceFactory(object):
    """
    """
    def __init__(self, hook_factory=BuildbotHookFactory()):
        self._hook_factory = hook_factory

    def make_services(self, config_dict=None):
        if config_dict is None:
            raise RuntimeError('config_dict cannot be None')
        _services = []
        if 'poll-interval' in config_dict:
            poll_interval = float(eval(config_dict['poll-interval']))
        else:
            poll_interval = self._poll_interval_default
        if not 'basedir' in config_dict:
            sys.exit('Required config item missing from org: basedir\n')
        basedir = config_dict['basedir']
        if 'subdir' in config_dict:
            destdir = basedir + '/' + config_dict['subdir']
        else:
            destdir = basedir
        bb_hook = self._hook_factory.make_buildbothook(config_dict)
        # Create objects to fetch git stuff specific to 'type' from config.
        fetch_type = config_dict['type']
        if fetch_type == 'git':
            if not 'url' in config_dict:
               sys.exit('Required section missing from git section: url\n')
            fetcher = GitFetcher(repo_url = config_dict['url'],
                                 hook = bb_hook,
                                 basedir = destdir)
        elif fetch_type == 'org':
            # sanity check GitHub org config
            if not 'name' in config_dict:
                sys.exit('Required section missing from org: name\n')
            # make the fetcher
            fetcher = GitHubOrgFetcher(orgname = config_dict ['name'],
                                       destdir = destdir,
                                       hook = bb_hook,
                                       poll_interval = poll_interval)
            _services.append(fetcher)
        else:
            raise NotImplementedError('Config section type {0} is not implemented.\n'.format(fetch_type))
        log.msg('Creating GitPollerService for fetcher {0}'.format(type(fetcher).__name__))
        fetcher_service = GitPollerService(poller=fetcher, step=poll_interval)
        _services.append(fetcher_service)
        return _services
