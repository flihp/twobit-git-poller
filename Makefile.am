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
	$(plugin)/twobit_poller_plugin.py

MOSTLYCLEANFILES = *pyc *pyo

# install tac / config files and create necessary directories
tacconfdir = $(sysconfdir)/twobit-gitpoller
tacconffile = src/twobit-gitpoller.conf
tacconfpath = $(tacconfdir)/twobit-gitpoller.conf
tacconf_DATA = $(tacconffile)
taclogdir = $(localstatedir)/log/twobit-gitpoller
taclibdir = $(localstatedir)/lib/twobit-gitpoller
tacrundir = $(localstatedir)/run/
# this isn't portable
initdir = $(sysconfdir)/init.d
init_SCRIPTS = src/twobit-gitpoller.init
EXTRA_SCRIPTS = src/twobit-gitpoller.init.in
tacpidfile = $(localstatedir)/run/twobit-gitpoller.pid
CLEANFILES = $(tacconf_DATA) $(init_SCRIPTS)
SUFFIXES = .in

$(tacconffile): $(tacconffile).in Makefile

.in:
	$(do_subst) < $< > $@

do_subst = sed -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
               -e 's,[@]CONFFILE[@],$(tacconfpath),g' \
               -e 's,[@]LOGDIR[@],$(taclogdir),g' \
               -e 's,[@]LIBDIR[@],$(taclibdir),g' \
               -e 's,[@]PIDFILE[@],$(tacpidfile),g'

# There's gotta be an easier way to do this
install-data-hook: mklogdir mklibdir mkrundir
uninstall-hook: rmlogdir rmlibdir rmrundir

mklogdir:
	mkdir -p $(DESTDIR)/$(taclogdir)
rmlogdir:
	-rmdir $(DESTDIR)/$(taclogdir)
mklibdir:
	mkdir -p $(DESTDIR)/$(taclibdir)
rmlibdir:
	-rmdir $(DESTDIR)/$(taclibdir)
mkrundir:
	mkdir -p $(DESTDIR)/$(tacrundir)
rmrundir:
	-rm -f $(DESTDIR)/$(tacpidfile)
