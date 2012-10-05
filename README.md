# django-mongolier

A lightweight toolkit for integrating MongoDB with Django

## Why?

django-mongolier is a wrapper for `pymongo` that adds many of the happy django bits for using mongodb in a normal django app.

You don't need any sort of special django-nosql or anything else, all you need is django >=1.31 and pymongo (and django-tastypie<=0.9.11 for the apis).

The goal of this was to only abstract out the annoying bits (AutoReconnect exceptions, mainly) while leaving the standard
query syntax of `pymongo` in.

## What's included

* db.py - a connection object for connecting to mongo instances and executing queries
* views.py - a lightweight replication of Django's class-based views for MongoDB
* api.py - a lightweight implementation of django-tastypie and mongodb (django-tastypie required)
* utils - a series of classes to filter python objects so they can be inserted into mongo
* fixture creation and database 'syncing' via standard Django management commands

## RoadMap (v 0.3.0)

* improved views, with more facets and mixins
* improved management commands

## Getting started

### Make a connection

```python

from mongolier import PersistentConnection
my_connection_object = PersistentConnection(database='face', collection='palm', auth='my_user:awesome_password')
my_connection_object.api.find({'query_param': 'query_value'})

```

### Query

Query like you would any other `pymongo` query

```python

my_mongo_cursor = mongo.find( {'query_key': query_value} )

```

Check out the [API docs](http://washingtonpost.github.com/django-mongolier "API documentation") for a more detailed README


# Changelog

## 0.3.0

### Backwards incompatible changes

* [db.py | removed] MongoConnection and PersistentConnection Aliases
* [views.py | deprecated and removed] Nonstandard connection object, replaced with single object from db.py
* [views.py | deprecated and removed] Strange parameter names, replaced with simpler names

### Bugfixes ###

* [views.py] Query parameters in url actually work now
* [api.py] Added ``key`` to ignored query parameters.
* [db.py] Fixed Connection object to reject other connection types after one has already been established. There is a pymongo bug where if you add a normal document to a gridfs collection, you can damage that collection.


### Features  ###

* [views.py] Added ``PagelessListView``
* [views.py] Vastly improved the views

## 0.2.0

### Backwards incompatible changes

* [db.py | deprecated and removed] auth kwarg inside MongoConnection/Connection objects
* [api.py | deprecated and removed] support for MongoConnection objects inside api.py
* [db.py | deprecated] MongoConnection and PersistentConnection Aliases (will be removed in 0.3.0)

### Features

* [db.py] Added support for additional kwargs to Connection object (for passing things like ``tags_set`` and ``read_preference``)
* [api.py] Added additional query style: ability to pass JSON objects into individual params
* [tests] Added working django test app

### Bugfixes

* [api.py] Corrected CREATE/UPDATE methods


## Pre 0.2.0

Early development, lots of changes too numerous to list here