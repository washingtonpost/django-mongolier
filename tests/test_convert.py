import unittest
import datetime
from decimal import Decimal

from mongolier.utils import convert


class TestConversion(unittest.TestCase):
    """
    Test the connection objects
    """

    iterable = {'decimal': ['list', 'of',  Decimal('20.01')],
                'unicode': u'a unicode string',
                'date': datetime.date(2012, 1, 2)
    }

    def test_decimal_conversion(self):
        """
        Test the conversion of decimal objects inside an iterable.
        """
        decimal_converter = convert.ConvertDecimal()

        converted = decimal_converter.convert(self.iterable)

        self.assertEqual(converted['decimal'][2], '20.01')
        self.assertEqual(converted['unicode'], u'a unicode string')
        self.assertEqual(converted['date'], datetime.date(2012, 1, 2))

    def test_decimal_conversion_float(self):
        """
        Test the conversion of decimal objects inside an iterable to a float
        """
        decimal_converter = convert.ConvertDecimal(to_float=True)

        converted = decimal_converter.convert(self.iterable)

        self.assertEqual(converted['decimal'][2], 20.01)
        self.assertEqual(converted['unicode'], u'a unicode string')
        self.assertEqual(converted['date'], datetime.date(2012, 1, 2))


    def test_deserializer(self):
        """
        Test the standard deserializer
        """
        deserializer = convert.Deserializer()

        converted = deserializer.convert(self.iterable)

        self.assertEqual(converted['decimal'][2], '20.01')
        self.assertEqual(converted['unicode'], 'a unicode string')
        self.assertNotEqual(type(converted['unicode']), unicode)
        self.assertEqual(converted['date'], '2012-01-02')
        self.assertNotEqual(type(converted['date']), datetime.date)


class TestClassOverride(TestConversion):
    """
    Test overriding a base conversion class, adding new methods, and running
    that conversion.
    """

    def test(self):

        class TestDeserializer(convert.BaseConvert):

            def __init__(self, **kwargs):
                super(TestDeserializer, self).__init__(**kwargs)

                self.other_input = {
                    datetime.date: self.decode_date,
                }

            def decode_date(self, date_obj):

                return(datetime.datetime.strftime(datetime.date(2012,1,20),
                                                    '%Y'))

        deserializer = TestDeserializer()

        converted = deserializer.convert(self.iterable)
        self.assertEqual(converted['date'], '2012')
        self.assertNotEqual(type(converted['date']), datetime.date)
