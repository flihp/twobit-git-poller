import ast, os, sys

from ConfigParser import ConfigParser
# from exception import RuntimeError, FileNotFoundError
from twisted.application.internet import TimerService
from twisted.application.service import IService, IServiceCollection, MultiService
from twisted.python import log
from twobit_gitpoller import BuildbotHook, GitFetcher, GitHubOrgFetcher
from zope.interface import implements

class TwobitGitPoller(object, MultiService):
    implements(IService, IServiceCollection)
    """
    """
    def __init__(self):
        MultiService.__init__(self)
        print('TwobitGitPoller __init__')

    def add_config(self, conf_file=None):
        log.msg('TwobitGitPoller.add_config')
        if conf_file is None:
            raise RuntimeError('No config file provieded')
        if not os.path.isfile(conf_file):
            raise IOError("Config file doesn't exist: {0}".format(conf_file))
        # get application config values
        self._config = ConfigParser()
        self._config.read(conf_file)
        self._logdir = self._config.get('DEFAULT', 'logdir')
        self._logfile = self._config.get('DEFAULT', 'logfile')
        # conservative default polling interval
        self._poll_interval_default = 1200

    def startService(self):
        """ load_config(self):

        This needs to be broken down.
        """
        log.msg('TwobitGitPoller.load__config')
        # Iterate over repos from config file
        for section in self._config.sections():
            # Get config values, use defaults if necessary.
            config_dict = dict(self._config.items(section))
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
            if ('hook-script' in config_dict and 'hook-master' in config_dict and
                'hook-port' in config_dict and 'hook-user' in config_dict and
                'hook-passwd' in config_dict and 'hook-projects' in config_dict):
                # Get hook script data. Assume all data is required until we find
                # a counter example.
                bb_hook = BuildbotHook(
                              script=config_dict['hook-script'],
                              host=config_dict['hook-master'],
                              port=config_dict['hook-port'],
                              user=config_dict['hook-user'],
                              passwd=config_dict['hook-passwd'],
                              logfile=config_dict['hook-logfile'],
                              projects=ast.literal_eval(config_dict['hook-projects'])
                          )
            else:
                bb_hook = None

            # Create objects to fetch git stuff specific to 'type' from config.
            fetch_type = self._config.get(section, 'type')
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
                fetcher = GitHubOrgFetcher(parent = self,
                                           orgname = config_dict ['name'],
                                           destdir = destdir,
                                           hook = bb_hook,
                                           poll_interval = poll_interval)
            else:
                raise NotImplementedError('Config section type {0} is not implemented.\n'.format(fetch_type))
            log.msg('Creating TimerService for fetcher {0}'.format(type(fetcher).__name__))
            loopreact = TimerService(step=poll_interval,
                                     callable=fetcher.poll)
            loopreact.setServiceParent(self)
            loopreact.startService()
