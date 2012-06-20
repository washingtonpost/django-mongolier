# django-mongolier

A lightweight toolkit for integrating MongoDB with Django

## Why?

django-mongolier is a wrapper for `pymongo` that adds many of the happy django bits for using mongodb in a normal django app.

You don't need any sort of special django-nosql or anything else, all you need is django >=1.31 and pymongo (and django-tastypie for the apis)

The goal of this was to only abstract out the annoying bits (AutoReconnect exceptions, mainly) while leaving the fairly intuitive
query syntax of `pymongo` in.

## What's included

* db.py - a connection object for connecting to mongo instances and executing queries
* views.py - a lightweight replication of Django's class-based views for MongoDB
* api.py - a lightweight implementation of django-tastypie and mongodb (django-tastypie required)
* utils.ConvertDecimal - a class for converting decimal objects into strings or floats so they can be inserted into mongo
* fixture creation and database 'syncing'

## RoadMap

* better error handling
* better/persistent connection objects

## Getting started

### Make a connection

```python

from mongolier import MongoConnection
my_connection_object = MongoConnection(database='face', collection='palm', auth='username:pass')
mongo = my_connection_object.connect()

```

### Query

Query like you would any other `pymongo` query

```python

my_mongo_cursor = mongo.find( {'query_key': query_value} )

```

### Management Commands (fixtures)

Available options

* '-d', '--database' -- MongoDB database name
* '-c', '--collection' -- MongoDB collection name
* '-a', '--auth' -- MongoDB auth (user:password)
* '-o', '--respect_objectid' -- Will retain original ObjectId (default: False)

#### Dump fixtures

	django-admin.py mongolier_dumpdata --database face --collection palm --auth 'username:pass' > /path/to/my/file.json

#### Load fixtures

	django-admin.py mongolier_loaddata --database face --collection palm --auth 'username:pass' /path/to/my/file.json



## Views

Check out `docs.detailed_readme.md`

## API

`coming soon`

## Utilities

`coming soon`
