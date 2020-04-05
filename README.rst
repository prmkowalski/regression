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

.. image:: https://github.com/makr3la/regression/workflows/CI/badge.svg
    :target: https://github.com/makr3la/regression/actions?query=workflow%3ACI

Web app for
`regression analysis <https://en.wikipedia.org/wiki/Regression_analysis>`_
of provided data files

`Changelog » <https://github.com/makr3la/regression/releases>`_

Installation
------------

Install with `pip <https://pip.pypa.io/en/stable/>`_:

.. code:: bash

    $ pip install regression

Usage
-----

To open ``config.cfg`` file and change configuration
`values <https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values>`_
run:

.. code:: bash

    $ regression config

Deploy web app to a WSGI server or run locally on Flask's built-in server:

.. code:: bash

    $ regression run

.. image:: https://repl.it/badge/github/makr3la/regression
   :target: https://repl.it/github/makr3la/regression

Files
-----

1. Provide your data files in one of the following ways:

- using **upload form**, which will save the file in the app root directory,

- by **copying them** into into the app subdirectory
  (run ``$ regression path`` to find the copy path),

- by **adding links** to files stored online as `URL` dict of config file:

.. code:: bash

    $ regression config
    ...
    URL = {'name': 'download_link'} # 'name' supports HTML format

2. Supported file formats and extensions:

- Delimited text files (CSV)

.. code:: bash

    index,features,...,outcome  # First row is a header
    item 1,X11,X12,...,X1p,y1   # Follow order: index, X, y
    item 2,X21,X22,...,X2p,y2   # Features can be given as
    ...                         # numerical or categorical
    item n,Xn1,Xn2,...,Xnp,yn   # Use ';' when decimal sep is ','

- Excel files (XLS, XLSX)

+--------+-----------+-----+-----------+---------+
|  index | feature 1 | ... | feature p | outcome |
+========+===========+=====+===========+=========+
| item 1 |    X11    | ... |    X1p    |    y1   |
+--------+-----------+-----+-----------+---------+
| item 2 |    X21    | ... |    X2p    |    y2   |
+--------+-----------+-----+-----------+---------+
|   ...  |    ...    | ... |    ...    |   ...   |
+--------+-----------+-----+-----------+---------+
| item n |    Xn1    | ... |    Xnp    |    yn   |
+--------+-----------+-----+-----------+---------+

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.
