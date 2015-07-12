pkgpython_PYTHON = \
    __init__.py \
    buildbot_hook.py \
    gitfetcher.py \
    github_orgfetcher.py

pkgpythondir = $(pythondir)/@PACKAGE@/
MOSTLYCLEANFILES = *pyc *pyo

TGP_PY_MODPATH = "../"

pylint:
	PYTHONPATH=$(TGP_PY_MODPATH) pylint $(pkgpython_PYTHON) > pylint.out
