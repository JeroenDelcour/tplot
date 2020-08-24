from .figure import Figure
try:
	from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

try:
    __version__ = version(__name__)
except:
    pass
