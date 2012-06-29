Getting Started
===============

Make a connection
-----------------

::

    from mongolier import MongoConnection
    my_connection_object = MongoConnection(database='face', collection='palm', auth='username:pass')
    mongo = my_connection_object.connect()

Query
-----

Query like you would any other `pymongo` query

::

    my_mongo_cursor = mongo.find( {'query_key': query_value} )