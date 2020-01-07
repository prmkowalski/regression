from setuptools import setup, find_packages

from regression import __version__, __doc__, __author__

setup(
    name='regression',
    version=__version__,
    description=__doc__.splitlines()[1],
    long_description=__doc__,
    url='https://github.com/makr3la/regression',
    author=__author__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Environment :: Web Environment',
        'Framework :: Flask',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'pandas>=0.24.0',
        'statsmodels',
    ],
    include_package_data=True,
    zip_safe=False,
)
