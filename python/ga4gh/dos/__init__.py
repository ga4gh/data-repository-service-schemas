"""
This module places the server and client modules in the `dos` namespace.
The :mod:`ga4gh.dos.server` implements a minimalistic DOS, which
interprets the schemas and allows one to test features. The
:mod:`ga4gh.dos.client` can be used to easily access DOS using named
Python functions.
"""

import client
import server

assert server
assert client
