from os import path

from setuptools import setup, find_packages
import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='regression',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Web app for regression analysis of provided data files',
    long_description=long_description,
    url='https://github.com/makr3la/regression',
    author='Paweł Kowalski',
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
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'openpyxl>=2.5.7',
        'pandas',
        'statsmodels',
        'xlrd>=1.1',
    ],
    extras_require={
        'test': ['pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'regression=regression.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
