import os

from setuptools import setup, find_packages

from regression import __version__, __doc__, __author__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f.readlines()]

setup(
    name='regression',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    url='https://github.com/makr3la/regression',
    author=__author__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
