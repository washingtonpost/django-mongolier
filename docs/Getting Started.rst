Getting Started
===============

Make a connection
-----------------

::

    from mongolier import Connection
    my_connection_object = Connection(database='face', collection='palm', auth='username:pass')

Query
-----

Query like you would any other `pymongo` query

::

    my_mongo_cursor = mongo.api.find({'query_key': query_value})

GridFS
------

Instead of using the ``api`` method, use gridfs to store objects as Grid objects.

::

    my_mongo_cursor = mongo.gridfs.put(really_big_dictionary)