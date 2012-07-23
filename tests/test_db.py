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

        connection.api.save({'mongolier-test': 1})

        data = connection.api.find_one({'mongolier-test': 1})

        self.assertEqual(data['mongolier-test'], 1)


class TestGrid(unittest.TestCase):
    """
    Test a gridfs connection
    """

    data = 'this is a string of test data'

    def test(self):
        """
        Test putting a item via GridFS, then check to see if it exists.
        """

        connection = Connection(db='test', collection='test')

        connection.fs.put(self.data, **{'mongolier-grid-test': 1})

        self.assertEqual(connection.fs.exists({'mongolier-grid-test': 1}), True)
