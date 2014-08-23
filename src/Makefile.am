tacdatadir = $(pkgdatadir)
tacdata_DATA = @PACKAGE@.tac
tacconfdir = $(sysconfdir)/@PACKAGE@
tacconf_DATA = @PACKAGE@.conf
taclogdir = $(localstatedir)/log/@PACKAGE@
taclibdir = $(localstatedir)/lib/@PACKAGE@

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

