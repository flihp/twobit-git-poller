import ast, subprocess
import logging as log

class BuildbotHookError(Exception):
    def __init__(self, message):
        super(BuildbotHookError, self).__init__(message)

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

    def exec_hook(self, data=(), gitdir=None):
        """ Execute the hook script.

        The data parameter is a tripple of the branch name, the
        hash of the HEAD of this branch before an update, and the
        hash of the HEAD of the same branch after an update.

        NOTE: the data parameter should be a tripple:
              (symname, hash before update, hash after update)
        """
        if self.script is None:
            raise BuildbotHookError("No hook script to execute")
        if (self.projects is None or self.projects == ()):
            raise BuildBotHookError("No projects for hook script")
        for project in self.projects:
            log.info("executing hookscript {0} for project {1}"
                     .format(self.script, project))
            # TODO: build this command up with data available
            cmd = [self.script,
                   '--master={0}:{1}'.format(self.host,
                                             self.port),
                   '--username=' + self.user,
                   '--auth=' + self.passwd,
                   '--logfile=' + self.logfile,
                   '--verbose', '--verbose', '--verbose',
                   '--project=' + project]
            env = {'GIT_DIR' : gitdir}
            log.info("executing hook script: {0} with environment {1}"
                     .format(cmd, env))
            p = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE)
            p.stdin.write('{0} {1} {2}\n'
                          .format(data[1], data[2], data[0]))

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
