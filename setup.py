import os
import sys
from setuptools import setup, find_packages

packages = find_packages(exclude=['tests'])
requires = ['betamax >= 0.3.2']

try:
    from betamax_matchers import __version__
except ImportError:
    __version__ = ''

if not __version__:
    raise RuntimeError('Cannot import version information')

if sys.argv[-1] in ['submit', 'publish']:
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


def data_for(filename):
    with open(filename) as fd:
        content = fd.read()
    return content

setup(
    name="betamax-matchers",
    version=__version__,
    description="A VCR imitation for python-requests",
    long_description="\n\n".join([data_for("README.rst"),
                                  data_for("HISTORY.rst")]),
    license=data_for('LICENSE'),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github.com/sigmavirus24/betamax_matchers",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
