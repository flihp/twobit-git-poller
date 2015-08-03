from twisted.python import log
from twobit_gitpoller import BuildbotHookFactory, GitPoller, GitHubOrgPoller, GitPollerService

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
        # Create objects to poll git stuff specific to 'type' from config.
        poller_type = config_dict['type']
        if poller_type == 'git':
            if not 'url' in config_dict:
               sys.exit('Required section missing from git section: url\n')
            poller = GitPoller(repo_url = config_dict['url'],
                               hook = bb_hook,
                               basedir = destdir)
        elif poller_type == 'org':
            # sanity check GitHub org config
            if not 'name' in config_dict:
                sys.exit('Required section missing from org: name\n')
            poller = GitHubOrgPoller(orgname = config_dict ['name'],
                                     destdir = destdir,
                                     hook = bb_hook,
                                     poll_interval = poll_interval)
            _services.append(poller)
        else:
            raise NotImplementedError('Config section type {0} is not implemented.\n'.format(poller_type))
        log.msg('Creating GitPollerService for poller {0}'.format(type(poller).__name__))
        _services.append(GitPollerService(poller=poller, step=poll_interval))
        return _services
