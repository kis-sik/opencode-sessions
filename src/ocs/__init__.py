"""OpenCode Sessions Manager - Enhanced session management for OpenCode"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("ocs")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "kis-sik"
__license__ = "MIT"