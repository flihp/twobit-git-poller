pkgplugindir = $(pythondir)/twisted/plugins
pkgplugin_PYTHON = twobit_gitpoller_plugin.py

MOSTLYCLEANFILES = *pyc *pyo

pylint:
	PYTHONPATH=../../../ pylint --errors-only $(pkgplugin_PYTHON) > pylint.out
