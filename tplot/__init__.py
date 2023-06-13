from importlib.metadata import version

from .figure import Figure

try:
    __version__ = version(__name__)
except NameError:
    pass
