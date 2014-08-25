# install tac / config files and create necessary directories
tacdatadir = $(pkgdatadir)
tacdata_DATA = @PACKAGE@.tac
tacconfdir = $(sysconfdir)/@PACKAGE@
tacconffile = @PACKAGE@.conf
tacconfpath = $(tacconfdir)/$(tacconffile)
tacconf_DATA = $(tacconffile)
taclogdir = $(localstatedir)/log/@PACKAGE@
taclibdir = $(localstatedir)/lib/@PACKAGE@
CLEANFILES = $(tacdata_DATA) $(tacconf_DATA)
SUFFIXES = .in

$(tacdata_DATA): $(tacdata_DATA).in Makefile
$(tacconf_DATA): $(tacconf_DATA).in Makefile

.in:
	$(do_subst) < $< > $@

do_subst = sed -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
               -e 's,[@]CONFFILE[@],$(tacconfpath),g' \
			   -e 's,[@]LOGDIR[@],$(taclogdir),g' \
			   -e 's,[@]LIBDIR[@],$(taclibdir),g'

# There's gotta be an easier way to do this
install-data-hook: mklogdir mklibdir
uninstall-hook: rmlogdir rmlibdir

mklogdir:
	mkdir -p $(taclogdir)
rmlogdir:
	@rmdir $(taclogdir)
mklibdir:
	mkdir -p $(taclibdir)
rmlibdir:
	@rmdir $(taclibdir)

