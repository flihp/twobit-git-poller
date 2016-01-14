buildbot = buildbotutil
buildbotdir = $(pythondir)/twobit/buildbotutil
buildbot_PYTHON = \
    $(buildbot)/__init__.py \
    $(buildbot)/buildbot_hook.py

gitutil = gitutil
gitutildir = $(pythondir)/twobit/gitutil
gitutil_PYTHON = \
    $(gitutil)/__init__.py \
	$(gitutil)/githuborg.py \
	$(gitutil)/githuborgrepopoller.py \
	$(gitutil)/gitpollerfactory.py \
	$(gitutil)/gitpoller.py \
    $(gitutil)/gitrepo.py \
	$(gitutil)/ipoll.py

twisted = twisted_gitpoller
twisted_pollerdir = $(pythondir)/twobit/twisted_gitpoller/
twisted_poller_PYTHON = \
    $(twisted)/__init__.py \
	$(twisted)/githuborgrepopollerservice.py \
	$(twisted)/gitpollerservice.py \
	$(twisted)/gitpollerservicefactory.py \
	$(twisted)/pollermultiservice.py

MOSTLYCLEANFILES = *pyc *pyo
