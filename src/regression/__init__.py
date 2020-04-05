__all__ = ['processing']
from ._version import version as __version__

from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

from . import views
