regression
==========

.. image:: https://img.shields.io/pypi/pyversions/regression
    :target: https://pypi.org/project/regression/
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/v/regression
    :target: https://pypi.org/project/regression/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/status/regression
    :target: https://pypi.org/project/regression/
    :alt: PyPI - Status

.. image:: https://img.shields.io/github/license/makr3la/regression
    :target: https://github.com/makr3la/regression/blob/master/LICENSE
    :alt: GitHub

.. image:: https://travis-ci.org/makr3la/regression.svg?branch=master
    :target: https://travis-ci.org/makr3la/regression

.. image:: https://coveralls.io/repos/github/makr3la/regression/badge.svg
    :target: https://coveralls.io/github/makr3la/regression

Web app for
`regression analysis <https://en.wikipedia.org/wiki/Regression_analysis>`_
of provided data files.

`Changelog » <https://github.com/makr3la/regression/releases>`_

Installation
------------

Install with `pip <https://pip.pypa.io/en/stable/>`_:

.. code:: bash

    $ pip install regression

Usage
-----

.. image:: https://repl.it/badge/github/makr3la/regression
   :target: https://repl.it/github/makr3la/regression

Deploy web app to a WSGI server or run locally on Flask's built-in server:

.. code:: bash

    $ python -m regression

Files
-----

Provide your data files either with upload form or by copying them into the app
root directory or subdirectory in one of the supported file formats:

- Delimited text files (CSV)

.. code:: bash

    index,features,...,outcome  # First row is a header containing a list of field names
    item 1,X11,X12,...,X1p,y1   # Value rows should follow this order
    item 2,X21,X22,...,X2p,y2   # Features can be given as numerical or categorical values
    ...
    item n,Xn1,Xn2,...,Xnp,yn

- Excel files (XLS, XLSX)

+--------+-----------------------+---------+
|  index |        features       | outcome |
+========+=====+=====+=====+=====+=========+
| item 1 | X11 | X12 | ... | X1p |    y1   |
+--------+-----+-----+-----+-----+---------+
| item 2 | X21 | X22 | ... | X2p |    y2   |
+--------+-----+-----+-----+-----+---------+
|   ...  | ... | ... | ... | ... |   ...   |
+--------+-----+-----+-----+-----+---------+
| item n | Xn1 | Xn2 | ... | Xnp |    yn   |
+--------+-----+-----+-----+-----+---------+

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.
