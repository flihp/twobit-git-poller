SUBDIRS = src src/twobit_gitpoller

base = $(srcdir)/src
twobit = $(base)/twobit
twobitdir = $(pythondir)/twobit
twobit_PYTHON = $(twobit)/__init__.py

buildbot = $(twobit)/buildbotutil
buildbotdir = $(pythondir)/twobit/buildbotutil
buildbot_PYTHON = \
    $(buildbot)/__init__.py \
    $(buildbot)/buildbot_hook.py

gitutil = $(twobit)/gitutil
gitutildir = $(pythondir)/twobit/gitutil
gitutil_PYTHON = \
    $(gitutil)/__init__.py \
	$(gitutil)/githuborg.py \
	$(gitutil)/githuborgrepopoller.py \
	$(gitutil)/gitpollerfactory.py \
	$(gitutil)/gitpoller.py \
    $(gitutil)/gitrepo.py \
	$(gitutil)/ipoll.py

twisted = $(twobit)/twisted_gitpoller
twisted_pollerdir = $(pythondir)/twobit/twisted_gitpoller/
twisted_poller_PYTHON = \
    $(twisted)/__init__.py \
	$(twisted)/githuborgrepopollerservice.py \
	$(twisted)/gitpollerservice.py \
	$(twisted)/gitpollerservicefactory.py \
	$(twisted)/pollermultiservice.py
plugin = $(base)/twisted/plugins
plugindir = $(pythondir)/twisted/plugins
plugin_PYTHON = \
    $(plugin)/twobit_gitpoller_plugin.py \
	$(plugin)/twobit_poller_plugin.py

MOSTLYCLEANFILES = *pyc *pyo
