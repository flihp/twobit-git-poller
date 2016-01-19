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

    def exec_hook(self, tripples=[], gitdir=None):
        """ Execute the hook script.

        The 'tripples' parameter is a list of tripples. Each tripple is
        in the form:  branch name, the hash of the HEAD of this branch
        before the update, and the hash of the HEAD of the same branch
        after an update.

        NOTE: each tripple is in the form:
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
            for tripple in tripples:
                p.stdin.write('{0} {1} {2}\n'
                              .format(tripple[1], tripple[2], tripple[0]))
            p.stdin.close()
            p.wait()

class BuildbotHookFactoryValueError(Exception):
    def __init__(self, message):
        super(BuildbotHookFactoryValueError, self).__init__("Missing "
            "require value in config dictionary: {0}".format(message))

class BuildbotHookFactory(object):
    """ BuildbotHookFactory

    Create BuildbotHook from config section.
    """
    def make_buildbothook(self, config_dict={}):
        if 'hook-logfile' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-logfile')
        if 'hook-master' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-master')
        if 'hook-passwd' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-passwd')
        if 'hook-port' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-port')
        if 'hook-projects' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-projects')
        if 'hook-script' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-script')
        if 'hook-user' not in config_dict:
            raise BuildbotHookFactoryValueError('hook-user')
        # Get hook script data. Assume all data is required until we find
        # a counter example.
        return BuildbotHook(script=config_dict['hook-script'],
                            host=config_dict['hook-master'],
                            port=config_dict['hook-port'],
                            user=config_dict['hook-user'],
                            passwd=config_dict['hook-passwd'],
                            logfile=config_dict['hook-logfile'],
                            projects=ast.literal_eval(config_dict['hook-projects']))
