#!/usr/bin/env python
from distutils.core import setup

setup(name='django-mongolier',
        version='0.0.3',
        description='A lightweight wrapper for using django with MongoDB (pymongo)',
        author='Jason Bartz & Jeremy Bowers',
        author_email=['bartzj@washpost.com','bowersj@washpost.com'],
        url='https://github.com/wpmedia/django-mongolier',
        packages = ['mongolier',],
        license = 'MIT',
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
)