# install tac / config files and create necessary directories
tacconfdir = $(sysconfdir)/twobit-gitpoller
tacconffile = twobit-gitpoller.conf
tacconfpath = $(tacconfdir)/$(tacconffile)
tacconf_DATA = $(tacconffile)
taclogdir = $(localstatedir)/log/twobit-gitpoller
taclibdir = $(localstatedir)/lib/twobit-gitpoller
tacrundir = $(localstatedir)/run/
# this isn't portable
initdir = $(sysconfdir)/init.d
init_SCRIPTS = twobit-gitpoller.init
EXTRA_SCRIPTS = twobit-gitpoller.init.in
tacpidfile = $(localstatedir)/run/twobit-gitpoller.pid
CLEANFILES = $(tacconf_DATA) $(init_SCRIPTS)
SUFFIXES = .in

$(tacconf_DATA): $(tacconf_DATA).in Makefile

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
	mkdir -p $(taclogdir)
rmlogdir:
	-rmdir $(taclogdir)
mklibdir:
	mkdir -p $(taclibdir)
rmlibdir:
	-rmdir $(taclibdir)
mkrundir:
	mkdir -p $(tacrundir)
rmrundir:
	-rm -f $(tacpidfile)
