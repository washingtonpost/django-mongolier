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
* api.py - a lightweight implementation of django-tastypie and mongodb (django-tastypie required) [readonly at the moment]
* utils.ConvertDecimal - a class for converting decimal objects into strings or floats so they can be inserted into mongo

## RoadMap

* fully editable api (POST, PATCH, DELETE)
* better error handling
* fixture creation and database 'syncing'

## Getting started

### Make a connection

    from mongolier import MongoConnection
    my_connection_object = MongoConnection(database='face', collection='palm', auth='username:pass')
    mongo = my_connection_object.connect()

### Query

Query like you would any other `pymongo` query

    my_mongo_cursor = mongo.find( {'query_key': query_value} )

## Views

Check out `docs.detailed_readme.md`

## API

`coming soon`

## Utils

`coming soon`

### ConvertDecimal

`coming soon`