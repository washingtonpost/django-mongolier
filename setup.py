#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import mongolier

setup(name='django-mongolier',
        version=mongolier.__version__,
        description='A lightweight wrapper for using django with MongoDB (pymongo)',
        author=mongolier.__author__,
        author_email=mongolier.__author_email__,
        url='https://github.com/wpmedia/django-mongolier',
        packages=['mongolier','mongolier.utils'],
        install_requires=['pymongo',],
        license=mongolier.__license__,
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
)