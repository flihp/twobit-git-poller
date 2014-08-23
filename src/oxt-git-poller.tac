# This program is the OpenXT git fetcher. It's a simple twisted
# application that periodically polls the specified git repos.
# Copyright (C) 2014  Philip Tricca <flihp@twobit.us>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This tac file defines an application that periodically fetches a collection of
git repos.
"""

from __future__ import print_function

import os, subprocess, sys
from ConfigParser import ConfigParser
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

# get application config values
config = ConfigParser ()
config.read ("/etc/oxt-git-poller/oxt-git-poller.conf")
gitdir = config.get ("default", "gitdir")
logdir = config.get ("default", "logdir")
logfile = config.get ("default", "logfile")
# use eval here to allow intervals like 60*5 to get 5 minutes
poll_interval = float (eval (config.get ("default", "poll-interval")))

logfile = DailyLogFile(logfile, logdir)
application = service.Application("OpenXT Git Poller")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

os.chdir(gitdir)
# Iterate over repos from config file
# For each: create GitFetcher that will poll on top level interval
for repo_tuple in config.items ('repos'):
    logfile.write ("Creating fetcher for {0} with URL {1}\n".format (repo_tuple [0], repo_tuple [1]))
    fetcher = GitFetcher (repo_tuple[1], gitdir)
    loopreact = internet.TimerService (step=poll_interval,
                                       callable=fetcher.poll)
    loopreact.setServiceParent (application)

