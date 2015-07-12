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
