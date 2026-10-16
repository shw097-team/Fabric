"""Import-time guard for the W3 solution suite (mandatory-defect 4).

Run as ``python -m pytest`` from ``candidate/solution/`` the interpreter puts the
current directory on ``sys.path`` first, so ``site`` imports THIS module before
pytest or its ``conftest.py`` is ever loaded. We set ``sys.dont_write_bytecode``
here so that not even ``tests/conftest.py`` itself is allowed to drop a
``__pycache__/*.pyc`` inside the deliverable. (A guard placed inside
``conftest.py`` runs too late: CPython writes a module's ``.pyc`` before it
executes the module body.)

This does not affect a lane: it is a no-op outside this test tree.
"""

import sys

sys.dont_write_bytecode = True
