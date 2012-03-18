bin_SCRIPTS = oh3c
oh3c:
	echo "#!/bin/sh"                       > $@
	echo "python $(pkgpythondir)/oh3c.py" >> $@
CLEANFILES = $(bin_SCRIPTS)

python_PYTHON = $(NULL)
pkgpython_PYTHON = $(NULL)
pkgpython_PYTHON += oh3c.py
pkgpython_PYTHON += __init__.py
pkgpython_PYTHON += eapauth.py
pkgpython_PYTHON += eappacket.py
pkgpython_PYTHON += macmgr.py
pkgpython_PYTHON += usermgr.py

