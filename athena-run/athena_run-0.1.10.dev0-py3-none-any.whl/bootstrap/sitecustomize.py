"""
Bootstrapping code that is run when using the `athena-run` Python entrypoint
Add all monkey-patching that needs to run by default here
"""
from __future__ import print_function

try:
    from patch import patch_all; patch_all() # noqa
except Exception as e:
    print("error configuring Athena tracing")

