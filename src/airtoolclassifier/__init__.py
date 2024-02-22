from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("AIrToolClassifier")
except PackageNotFoundError:
    __version__ = "unknown"
