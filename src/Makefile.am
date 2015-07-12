# install tac / config files and create necessary directories
tacdatadir = $(pkgdatadir)
tacdata_DATA = twobit-git-poller.tac
tacconfdir = $(sysconfdir)/twobit-git-poller
tacconffile = twobit-git-poller.conf
tacconfpath = $(tacconfdir)/$(tacconffile)
tacconf_DATA = $(tacconffile)
taclogdir = $(localstatedir)/log/twobit-git-poller
taclibdir = $(localstatedir)/lib/twobit-git-poller
tacrundir = $(localstatedir)/run/
tacfile = $(tacdatadir)/$(tacdata_DATA)
# this isn't portable
initdir = $(sysconfdir)/init.d
init_SCRIPTS = twobit-git-poller.init
EXTRA_SCRIPTS = twobit-git-poller.init.in
tacpidfile = $(localstatedir)/run/twobit-git-poller.pid
CLEANFILES = $(tacdata_DATA) $(tacconf_DATA) $(init_SCRIPTS)
SUFFIXES = .in

$(tacdata_DATA): $(tacdata_DATA).in Makefile
$(tacconf_DATA): $(tacconf_DATA).in Makefile

.in:
	$(do_subst) < $< > $@

do_subst = sed -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
               -e 's,[@]CONFFILE[@],$(tacconfpath),g' \
			   -e 's,[@]LOGDIR[@],$(taclogdir),g' \
			   -e 's,[@]LIBDIR[@],$(taclibdir),g' \
			   -e 's,[@]PIDFILE[@],$(tacpidfile),g' \
			   -e 's,[@]TACFILE[@],$(tacfile),g'

# There's gotta be an easier way to do this
install-data-hook: mklogdir mklibdir mkrundir
uninstall-hook: rmlogdir rmlibdir rmrundir

mklogdir:
	mkdir -p $(taclogdir)
rmlogdir:
	@rmdir $(taclogdir)
mklibdir:
	mkdir -p $(taclibdir)
rmlibdir:
	@rmdir $(taclibdir)
mkrundir:
	mkdir -p $(tacrundir)
rmrundir:
	@rmdir $(tacrundir)

