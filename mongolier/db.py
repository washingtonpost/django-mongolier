'''
A base class for connecting to the Post Mongo DB
    hosted on ec2 @ data.washingtonpost.com

Usage:

mongo_object = connect.MongoConnection(port=222, host='myhost')

mongo_connection = mongo_object.connect()

'''
import time
from pymongo import Connection
from pymongo.errors import AutoReconnect, ConnectionFailure, OperationFailure
from gridfs import GridFS
from common.mongo.exceptions import IncorrectParameters

class MongoConnection(object):
    
    def __init__(self, *args, **kwargs):
        '''
        Instantiate the Mongo class
        
        This can take up to four optional arguments, all of which help
            connect to the right database
            
        Optional args:
        :: port
        Port where you post Mongo data to
        :: localhost
        Mongo database host
        :: db
        Mongo db, a db is a series of collections
        :: auth
        A string that contains username and password, separated by :
        For example
            testuser:testpassword
        
        :: collection
        Collection, where the actual data is stored
        '''
        self.args = args
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
        if not kwargs.get('port'):
            self.port = 27017
            
        if not kwargs.get('host'):
            self.host = 'localhost'
            
        if not kwargs.get('db'):
            self.db = 'test_db'
            
        if not kwargs.get('collection'):
            self.collection = 'test_col'
            
        if not kwargs.get('auth'):
            self.auth = None

        if not kwargs.get('retries'):
            self.max_retries = 2
        
        self._retrires = 0

    def _connect_to_db(self):
        '''
        Connect to the database, but do not initialize a connection.
        
        Depending on which public method is used, it initiates either a standard
            mongo connection or a gridfs connection
        '''


        try:
            connection = Connection(self.host, self.port)
            
            database = connection[self.db]
            
            if self.auth is not None:
                self.auth = self.auth.split(':')
                if len(self.auth) != 2:
                    raise IncorrectParameters('Incorrect auth params, you passed %s' % self.auth)
                
                database.authenticate(self.auth[0], self.auth[1])
        except AutoReconnect, error_message:
            time.sleep(2)
            if self._retries <= self.max_retries:
                self._connect_to_db()
            else:
                raise ConnectionFailure('Max number of retries (%s) reached. Error: %s'\
                                         % (self.max_retries, error_message))
        except OperationFailure, error_message:
            time.sleep(2)
            if self._retries <= self.max_retries:
                self._connect_to_db()
            else:
                raise OperationFailure('Max number of retries (%s) reached. Error: %s'\
                                         % (self.max_retries, error_message))
        return database
        
    def connect(self):
        '''
        Connect to the mongo instance
        '''
        database = self._connect_to_db()

        collection = database[self.collection]
        
        return collection
    
    def gridfs(self):
        '''
        A module to connect to GridFS and chunk large files for saving into mongo
        '''
        database = self._connect_to_db()
        
        grid = GridFS(database, collection=self.collection)
        
        return grid
