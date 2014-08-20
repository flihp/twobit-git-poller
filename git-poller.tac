# You can run this .tac file directly with:
#    twistd -ny service.tac

"""
This tac file defines an application that periodically fetches a collection of
git repos.
"""

from __future__ import print_function

import os
import subprocess
from twisted.application import service, internet
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

basedir = "/tmp"

logfile = DailyLogFile("git-poller.log", "/tmp")

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Git Poller")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

class GitFetcher(object):
    """ Class to fetch git repos
    """
    def __init__(self, repolist = [], basedir = "/tmp"):
        self.repolist = repolist
        self.basedir = basedir + "/"

    def poll(self):
        if self.repolist is not {}:
            for repo_url in self.repolist:
                repo_name = repo_url.split("/")[-1].split(".")[0]
                repo_path = self.basedir + "/" + repo_name
                print("fetching repo %s from URL %s into %s", repo_name, repo_url, repo_path)
                try:
                    if not os.path.exists(repo_path):
                        subprocess.check_output(["git", "clone", repo_url],

        	                                stderr=subprocess.STDOUT)
                    elif os.path.isdir(repo_path):
                        os.chdir(repo_path)
                        subprocess.check_output(["git", "fetch"],
                                                stderr=subprocess.STDOUT)
                        os.chdir(self.basedir)
                    else:
                        print("%s exists but isn't a directory, bad news", repo_path)
                except subprocess.CalledProcessError, e:
                    print("%s", e)
                print("success polling repo: %s", repo_url)

        else:
            print("repolist is empty, nothing to poll")

gits = ["git://github.com/flihp/meta-measured.git"]
gitpoll = GitFetcher(gits, basedir)

os.chdir(basedir)
loopreact = internet.TimerService(step=60*5, callable=gitpoll.poll)
loopreact.setServiceParent(application)

