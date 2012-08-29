#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import mongolier
    # Import meta information
    version = mongolier.__version__
    author = mongolier.__author__
    license = mongolier.__license__
    email = mongolier.__author_email__

except ImportError:
    # Prevents failing if not all libs are installed.
    pass

setup(name='django-mongolier',
        version=version,
        description='A lightweight wrapper for using django with MongoDB (pymongo)',
        author=author,
        author_email=email,
        url='https://github.com/wpmedia/django-mongolier',
        packages=['mongolier','mongolier.utils'],
        install_requires=['pymongo',],
        license=license,
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
)