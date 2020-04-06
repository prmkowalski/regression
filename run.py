"""Run on Flask's built-in server."""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from regression.__main__ import main

if __name__ == '__main__':
    main(['run'])
