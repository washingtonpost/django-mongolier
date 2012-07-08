"""
fixtures.py

A module for creating json fixtures that can be imported into MongoDB and
exporting fixtures from MongoDB

"""
import sys
import json

from bson import json_util
from bson.objectid import ObjectId

class FixtureBase(object):
    """
    FixtureBase

    Currently only holds the connection object
    """

    def __init__(self, connection, respect_id=False):

        self.connection = connection
        self.respect_id = respect_id

class CreateFixture(FixtureBase):
    """
    Creates a fixture (json file) that is a representation of a
    MongoDB collection

    Uses a standard style to store objects.

    {'objectid_3344545aa4453445': ['foo','bar']}

    If respect_id is set to true, it will store the key prefaced
    (like above) so that when it restores objects, it retains their id.

    """

    def create(self):
        """
        Create a fixture file
        """
        fixture_dict = {}

        for document in self.connection.find():

            if isinstance(document['_id'], ObjectId) and self.respect_id:
                key = 'objectid_%s' % document['_id'].__str__()
            else:
                key = document['_id'].__str__()
            document.pop('_id')

            fixture_dict[key] = document


        sys.stdout.write(json.dumps(fixture_dict, default=json_util.default, indent=2))


class LoadFixture(FixtureBase):
    """
    Loads a fixture (json file) into MongoDB.

    """

    def load(self, fixture):
       """
       Load a fixture into MongoDB
       """
        with open(fixture, 'rb') as fixtures_file_obj:
            fixture_dict = json.load(fixtures_file_obj, object_hook=json_util.object_hook)

        for key, document in fixture_dict.items():
            if 'objectid_' in key and self.respect_id:
                document['_id'] = ObjectId(key.split('objectid_')[1])

            elif self.respect_id:
                document['_id'] = key

            self.connection.insert(document)