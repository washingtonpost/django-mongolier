"""
db.py

A class for connecting to a MongoDB instance
"""
import time
import pymongo
from pymongo.errors import (AutoReconnect,
                            ConnectionFailure,
                            OperationFailure,
                            InvalidMode)
from gridfs import GridFS


class BaseConnection(object):
    """
    The base methods used for all connection objects
    """
    def __init__(self,
                host='localhost',
                port=27017,
                db='test',
                collection='test',
                username=None,
                password=None,
                max_retries=2,
                **options):
        """
        Instantiate the Mongo class

        This can take optional arguments, all of which help
            connect to the right database

        """
        #: The port that the MongoDB connection lives on
        self.port = port

        #: The host or IP address to connect to
        self.host = host

        #: The name of the database
        self.db = db

        #: The name of the collection
        self.collection = collection

        #: The database username
        self.username = username

        #: The database password
        self.password = password

        #: The number of retries to attempt to reconnect after a connection
        #: is dropped.
        self.max_retries = max_retries

        # Additional options
        self.options = options

    def _connect_to_db(self, retries=0):
        """
        Connect to the database, but do not initialize a connection.

        Depending on which public method is used, it initiates either a standard
            mongo connection or a gridfs connection
        """
        retries = retries

        try:
            # Establish a Connection
            connection = pymongo.Connection(self.host, self.port, **self.options)

            # Establish a database
            database = connection[self.db]

            # If user passed username and password args, give that to authenticate
            if self.username and self.password:
                database.authenticate(self.username, self.password)

        # Handle the following exceptions, if retries is less than what is
        # passed into this method, attempt to connect again.  Otherwise,
        # raise the proper exception.
        except AutoReconnect, error_message:
            time.sleep(2)
            retries += 1

            if retries <= self.max_retries:
                self._connect_to_db(retries=retries)
            else:
                raise ConnectionFailure('Max number of retries (%s) reached. Error: %s'\
                                         % (self.max_retries, error_message))

        except OperationFailure, error_message:
            time.sleep(2)
            retries += 1

            if retries <= self.max_retries:
                self._connect_to_db(retries=retries)
            else:
                raise OperationFailure('Max number of retries (%s) reached. Error: %s'\
                                         % (self.max_retries, error_message))

        return database

    def _check_mode(self, mode):
        """
        Check mode is a failsafe designed to prevent bad operations from happening.

        Because pymongo (and MongoDB) can be finnicky when using a standard query
        to access a gridfs collection and visa versa, we put in a check that once
        a connection is made, it can only be that type of connection.
        """
        if mode is not self._mode:
            raise InvalidMode(".The mode set does not match the mode requested. \n\
                                This connection object already used %s" % mode)

    def _connect(self):
        """
        Connect to the mongo instance
        """
        self._check_mode('api')

        database = self._connect_to_db()

        collection = database[self.collection]

        return collection

    def _gridfs(self):
        """
        A module to connect to GridFS and chunk large files for saving into mongo
        """
        self._check_mode('gridfs')

        database = self._connect_to_db()

        grid = GridFS(database, collection=self.collection)

        return grid


class Connection(BaseConnection):
    """
    A wrapper for MongoConnection that stores a persistent set of connection information

    Import PersistentConnection from mongolier, and pass in the proper kwargs.

    ::

        my_connection = Connection(**{
            "database": "my_db",
            "collection": "my_collection",
            "port": 27017,
            "username": "my_login"
            "password": "my_pass",
            "retries": 5,
        })


    Inside your module, just pull in that connection and query against its api.

    ::

        from django.db.settings import my_connection
        my_connection.api.find_one({"query_param": "value"})

    For GridFS, use the gridfs API.

    >>> my_connection.gridfs.get_last_version(**{"query_param": "value"})
    """

    @property
    def api(self):
        self._mode = 'api'
        return(self._connect())

    @property
    def fs(self):
        self._mode = 'gridfs'
        return(self._gridfs())
