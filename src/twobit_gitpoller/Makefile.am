pkgpythondir = $(pythondir)/@PACKAGE@/
pkgpython_PYTHON = \
    __init__.py \
    buildbot_hook.py \
    gitpoller.py \
    github_orgpoller.py \
    gitpollerservice.py \
    gitpollerservicefactory.py \
    gitpollermultiservice.py \
    ipoll.py

MOSTLYCLEANFILES = *pyc *pyo

pylint:
	PYTHONPATH=../ pylint --errors-only $(pkgpython_PYTHON) > pylint.out
