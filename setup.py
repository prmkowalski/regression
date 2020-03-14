from os import path

from setuptools import setup, find_packages
import versioneer

from regression import __doc__, __author__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='regression',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=__doc__,
    long_description=long_description,
    url='https://github.com/makr3la/regression',
    author=__author__,
    author_email='makr3la@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'pandas',
        'scikit-learn',
        'xlrd>=1.1,<2',
    ],
    include_package_data=True,
    zip_safe=False,
)
