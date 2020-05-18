#!/usr/bin/env python3
"""
Sub-module required for the absolute import statements/paths to work in Python3.

Also where the hard-coded version string is stored.
NB: OF WHICH THERE CAN ONLY BE 1 (ONE)!!!
"""

# This value is not the one controlling the version in the (GitLab) pipeline
# This value is only necessary for automated pickup, and for manual deployments to PyPI
version = '1.1.4'
