#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='hashdial',
    version='0.1.0',
    description='A module implementing hash based decision making',
    long_description="""Implements, through hashing, decision making that is deterministic on input, but probabilistic across a set of inputs.

For example, suppose a set of components in a distributed system wish to emit a log entry for 1% of requests - but each
component should log the *same* 1% of requests, they could do so as such::

    if hashdial.decide(request.id, 0.01):
        log_request(request)
""",  # noqa
    long_description_content_type='text/x-rst',
    url='https://github.com/scode/py-hashdial',
    author='Peter Schuller',
    author_email='peter.schuller@infidyne.com',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hashdial',
    packages=find_packages(exclude=['docs', 'scripts', 'tests']),

    install_requires=[
    ],

    extras_require={
        # see requirements-dev.in/requirements-dev.txt
    },

    project_urls={
        'Documentation': 'http://py-hashdial.readthedocs.io/en/latest/',
        'Source': 'https://github.com/scode/py-hashdial',
    },
)
