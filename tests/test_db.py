import unittest

from mongolier import Connection
from mongolier.exceptions import InvalidMode


class TestConnection(unittest.TestCase):
    """
    Test the connection objects
    """

    def setUp(self):
        self.connection = Connection(db='test', collection='mongolier_test')

    def test(self):
        """
        Test connecting to a normal DB, and saving an item.
        """
        # Insert data
        self.connection.api.save({'mongolier-test': 1})

        # Find the data, make certain it was entered
        data = self.connection.api.find_one({'mongolier-test': 1})

        # Make sure the data is correct
        self.assertEqual(data['mongolier-test'], 1)

        # Test connecting to a different collection, via attribute and item access
        self.connection.mongolier_test2.save({'mongolier-test': 2})
        data_from_db_2 = self.connection['mongolier_test2'].find_one({'mongolier-test': 2})
        self.assertEqual(data_from_db_2['mongolier-test'], 2)

    def tearDown(self):
        # Destroy test data
        self.connection.api.drop()
        self.connection.mongolier_test2.drop()


class TestGrid(unittest.TestCase):
    """
    Test a gridfs connection
    """

    data = 'this is a string of test data'
    connection_info = {
        'db': 'test',
        'collection': 'gridtest'
    }

    def setUp(self):
        self.connection = Connection(**self.connection_info)

    def test(self):
        """
        Test putting a item via GridFS, then check to see if it exists.
        """
        # Put string data into grid
        self.connection.fs.put(self.data, **{'mongolier-grid-test': 1})

        # Make certain the data exists
        self.assertEqual(self.connection.fs.exists({'mongolier-grid-test': 1}), True)

        # Get the data using the kwargs
        receieved_data = self.connection.fs.get_last_version(**{'mongolier-grid-test': 1})

        # Make sure the data is correct
        self.assertEqual(receieved_data.read(), 'this is a string of test data')

        # Ensure that we cannot access the collection via API, after already
        # via grid
        with self.assertRaises(InvalidMode):
            self.connection.api.find()

    def tearDown(self):
        # Destroy test data
        connection = Connection(**self.connection_info)
        connection['gridtest.chunks'].drop()
        connection['gridtest.files'].drop()
