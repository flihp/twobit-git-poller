pkgpythondir = $(pythondir)/@PACKAGE@/
pkgpython_PYTHON = \
    __init__.py \
    buildbot_hook.py \
    gitfetcher.py \
    github_orgfetcher.py \
    gitpoller.py

MOSTLYCLEANFILES = *pyc *pyo

pylint:
	PYTHONPATH=../ pylint --errors-only $(pkgpython_PYTHON) > pylint.out
