"""Run on Flask's built-in server or configure."""

import argparse
import os
from threading import Timer
import webbrowser

from regression import app

parser = argparse.ArgumentParser()
parser.add_argument('--config', action='store_true',
                    help='open configuration file')
args = parser.parse_args()

if args.config:
    webbrowser.open(os.path.join(os.path.dirname(__file__), 'config.cfg'))
else:
    Timer(1, webbrowser.open_new('http://localhost:8080/')).start()
    app.run(host='0.0.0.0', port=8080, debug=False)
