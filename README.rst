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

.. image:: https://img.shields.io/travis/makr3la/regression
    :target: https://travis-ci.com/makr3la/regression
    :alt: Travis (.org)

Web app and library for
`regression analysis <https://en.wikipedia.org/wiki/Regression_analysis>`_
of provided data files.

`Changelog » <https://github.com/makr3la/regression/releases>`_

Installation
------------

Install with `pip <https://pip.pypa.io/en/stable/>`_:

.. code:: bash

    $ pip install regression

For web app use `git <https://git-scm.com/>`_ to clone GitHub repository:

.. code:: bash

    $ git clone git://github.com/makr3la/regression
    $ cd regression
    $ pip install -r requirements.txt

Check
`requirements.txt <https://github.com/makr3la/regression/blob/master/requirements.txt>`_
for dependencies.

Usage
-----

.. code:: python

    from regression import processing as lib

    files = lib.find_files()
    sample = {'feature_1': 'value', 'feature_2': 'value', 'feature_n': 'value'}

    X, y, sample = lib.process_data(files['data.csv'], sample)  # Ingest and format data
    lib.predict_ols(X, y, sample)  # Run OLS model
    lib.predict_gbr(X, y, sample)  # Run Gradient Boosting for regression model

Run web app on Flask's built-in server or deploy to a WSGI server:

.. code:: bash

    $ python run.py

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
