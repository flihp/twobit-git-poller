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

class GitFetcher(object):
    """ Class to fetch git repos
    """

    def __init__(self, repo_url = None, basedir = "/tmp"):
        self.repo_url = repo_url
        self.basedir = basedir
        self.repo_name = self.repo_url.split("/")[-1].split(".")[0]
        self.repo_path = self.basedir + "/" + self.repo_name

    def poll(self):
        if self.repo_url is not None:
            print("fetching repo {0} from URL {1} into {2}".format(self.repo_name, self.repo_url, self.repo_path))
            try:
                if not os.path.exists(self.repo_path):
                    os.chdir(self.basedir)
                    subprocess.check_output(["git", "clone", self.repo_url],
                                            stderr=subprocess.STDOUT)
                elif os.path.isdir(self.repo_path):
                    os.chdir(self.repo_path)
                    subprocess.check_output(["git", "fetch"],
                                            stderr=subprocess.STDOUT)
                    os.chdir(self.basedir)
                else:
                    print("{0} exists but isn't a directory, bad news".format(self.repo_path))
            except subprocess.CalledProcessError, e:
               print("{0}".format(e))
            print("success polling repo: {0}".format(self.repo_url))
        else:
            print("no repo url set, nothing to poll")

# this is the core part of any tac file, the creation of the root-level
# application object
logfile = DailyLogFile("git-poller.log", "/tmp")
application = service.Application("Git Poller")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

repos = ["git://github.com/flihp/meta-measured.git",
         "git://github.com/openembedded/openembedded-core.git",
         "git://git.yoctoproject.org/meta-intel"]
basedir = "/tmp"
os.chdir(basedir)
for repo in repos:
    print("Creating fetcher for {0}".format(repo))
    fetcher = GitFetcher (repo, basedir)
    loopreact = internet.TimerService (step=60, callable=fetcher.poll)
    loopreact.setServiceParent (application)

