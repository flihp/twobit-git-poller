import ast

class BuildbotHook(object):
    """ BuildbotHook class
    """

    def __init__(self, script=None, host=None, port=None, user=None,
                 passwd=None, projects=[], logfile=None):
        self.script = script
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.projects = projects
        self.logfile = logfile

class BuildbotHookFactory(object):
    """ BuildbotHookFactory

    Create BuildbotHook from config section.
    """
    @staticmethod
    def make_buildbothook(config_dict):
        if ('hook-script' in config_dict and 'hook-master' in config_dict and
            'hook-port' in config_dict and 'hook-user' in config_dict and
            'hook-passwd' in config_dict and 'hook-projects' in config_dict):
            # Get hook script data. Assume all data is required until we find
            # a counter example.
            return BuildbotHook(
                       script=config_dict['hook-script'],
                       host=config_dict['hook-master'],
                       port=config_dict['hook-port'],
                       user=config_dict['hook-user'],
                       passwd=config_dict['hook-passwd'],
                       logfile=config_dict['hook-logfile'],
                       projects=ast.literal_eval(config_dict['hook-projects'])
                   )
        else:
            return None
