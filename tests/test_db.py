import unittest

from mongolier import Connection


class TestConnection(unittest.TestCase):
    """
    Test the connection objects
    """

    def test(self):
        """
        Test connecting to a normal DB, and saving an item.
        """

        connection = Connection(db='test', collection='test')

        # Insert data
        connection.api.save({'mongolier-test': 1})

        # Find the data, make certain it was entered
        data = connection.api.find_one({'mongolier-test': 1})

        # Make sure the data is correct
        self.assertEqual(data['mongolier-test'], 1)

        # Destroy test data
        connection.api.remove({'mongolier-test': 1})

        # Test for __getattribute__ and __getitem__
        raise Exception("write __getattribute__ and __getitem__ test")


class TestGrid(unittest.TestCase):
    """
    Test a gridfs connection
    """

    data = 'this is a string of test data'

    def test(self):
        """
        Test putting a item via GridFS, then check to see if it exists.
        """

        connection = Connection(db='test', collection='gridtest')

        # Put string data into grid
        connection.fs.put(self.data, **{'mongolier-grid-test': 1})

        # Make certain the data exists
        self.assertEqual(connection.fs.exists({'mongolier-grid-test': 1}), True)

        # Get the data using the kwargs
        data = connection.fs.get_last_version(**{'mongolier-grid-test': 1})

        # Make sure the data is correct
        self.assertEqual(data.read(), 'this is a string of test data')

        # Destroy test data
        connection.fs.delete(data._id)
