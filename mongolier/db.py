"""
db.py

A class for connecting to a MongoDB instance
"""
import time
import pymongo
from pymongo.errors import AutoReconnect, ConnectionFailure, OperationFailure
from gridfs import GridFS
from mongolier.exceptions import IncorrectParameters
from warnings import warn


class BaseConnection(object):

    def __init__(self, *args, **kwargs):
        """
        Instantiate the Mongo class

        This can take optional arguments, all of which help
            connect to the right database

        """
        self.args = args

        for key, value in kwargs.items():
            setattr(self, key, value)

        #: The port that the MongoDB connection lives on
        if not kwargs.get('port'):
            self.port = 27017

        #: The host or IP address to connect to
        if not kwargs.get('host'):
            self.host = 'localhost'

        #: The name of the database
        if not kwargs.get('db'):
            self.db = 'test_db'

        #: The name of the collection
        if not kwargs.get('collection'):
            self.collection = 'test_col'

        #: DEPRECATED: Auth parameters `username:password`
        if not kwargs.get('auth'):
            self.auth = None

        #: The database username
        if not kwargs.get('username'):
            self.username = None

        #: The database password
        if not kwargs.get('password'):
            self.password = None

        #: The number of retries to attempt to reconnect after a connection
        # is dropped.
        if not kwargs.get('retries'):
            self.max_retries = 2

        deprecated = ['auth']

        # Check for deprecated kwargs, and warn accordingly
        for kwarg in deprecated:
            if kwarg in kwargs:
                warn('%s is deprecated and will be removed in v 0.2.0' % kwarg, DeprecationWarning)

    def _connect_to_db(self, retries=0):
        """
        Connect to the database, but do not initialize a connection.

        Depending on which public method is used, it initiates either a standard
            mongo connection or a gridfs connection
        """
        retries = retries

        try:
            # Establish a Connection
            connection = pymongo.Connection(self.host, self.port)

            # Establish a database
            database = connection[self.db]

            # If user passed username and password args, give that to authenticate
            if self.username and self.password:
                database.authenticate(self.auth[0], self.auth[1])

            # Else, look for the deprecated auth key
            elif self.auth is not None:
                try:
                    self.auth = self.auth.split(':')

                # If self.auth is already a list, just pass
                except AttributeError:
                    pass
                if len(self.auth) != 2:
                    raise IncorrectParameters('Incorrect auth params, you passed %s' % self.auth)

                database.authenticate(self.auth[0], self.auth[1])

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

    def connect(self):
        """
        Connect to the mongo instance
        """
        database = self._connect_to_db()

        collection = database[self.collection]

        return collection

    def gridfs(self):
        """
        A module to connect to GridFS and chunk large files for saving into mongo
        """
        database = self._connect_to_db()

        grid = GridFS(database, collection=self.collection)

        return grid


class MongoConnection(BaseConnection):
    """
    Alias for BaseConnection so we don't break backwards compatibility.
    """


class Connection(BaseConnection):
    """
    A wrapper for MongoConnection that stores a persistent set of connection information

    Import PersistentConnection from mongolier, and pass in the proper kwargs.

    ::

        my_connection = PersistentConnection(**{
            "database": "my_db",
            "collection": "my_collection",
            "port": 27017,
            "auth": "my_login:my_pass",
            "retries": 5,
        })


    Inside your module, just pull in that connection and query against its api.

    ::

        from django.db.settings import my_connection
        my_connection.api.find_one({"query_param": "value"})

    For GridFS, use the gridfs API.

    >>> my_connection.gridfs.get_last_version(**{"query_param": "value"})
    """

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

        self.fs = self.gridfs()

        self.api = self.connect()


class PersistentConnection(Connection):
    """
    Alias for Connection so we don't break backwards compatibility.
    """
