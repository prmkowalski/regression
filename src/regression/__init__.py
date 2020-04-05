__all__ = ['processing']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

from . import views
