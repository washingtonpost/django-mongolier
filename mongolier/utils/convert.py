"""
convert.py

Contains utilities and tools for pymongo
"""
from decimal import Decimal, getcontext
import datetime

from mongolier.exceptions import ValueNotSupported


class BaseConvert(object):
    """
    This object contains the base elements required to convert a python
    object into a Mongo object.

    Includes the methods decode_dict and decode_list

    You can pass a kwarg with additional types of input
    in order to have more parameters evaluated.

    `other_input` is a dictionary where the key is the object type to be evaluated
    and the value is the method call in which to evaluate the key against.

    """

    supported_iterables = [dict, list]

    def __init__(self, **kwargs):
        
        self.other_input = {}

    def decode_dict(self, input_dict):

        output_dict = {}

        for key, item in input_dict.items():
            if isinstance(item, list):
                item = self.decode_list(item)

            if isinstance(item, dict):
                item = self.decode_dict(item)

            for evaluation_type, evaluation_behavior in self.other_input.items():
                
                if isinstance(item, evaluation_type):
                    
                    item = evaluation_behavior(item)

            output_dict[key] = item
        
        return(output_dict)

    def decode_list(self, input_list):

        output_list = []

        for item in input_list:
            if isinstance(item, list):
                item = self.decode_list(item)

            if isinstance(item, dict):
                item = self.decode_dict(item)

            for evaluation_type, evaluation_behavior in self.other_input.items():
                
                if isinstance(item, evaluation_type):

                    item = evaluation_behavior(item)

            output_list.append(item)
        
        return(output_list)

    def convert(self, iterable):
        """
        Public method to convert.

        """

        if isinstance(iterable, list):
            output = self.decode_list(iterable)

        elif isinstance(iterable, dict):
            output = self.decode_dict(iterable)

        else:
            raise ValueNotSupported("The type of iterable you have passed is not currently supported. \n\
                                    You passed: %s\n\
                                    Please pass one of the following: %s " % 
                                    (iterable.__class__, self.supported_iterables))

        return(output)

class ConvertDecimal(BaseConvert):
    """
    A tool to handle python's Decimal objects
    and convert them to a type that MongoDB
    can handle.

    Default is to convert to strings

    You can select floats by passing float=True to the instantiation
    of the class.

    Support for dict, list

    Usage:

    >>> from common.mongo.utils import ConvertDecimal
    >>> my_list = [
    ...     Decimal('111223.22')
    ... ]
    >>> converted_list = ConvertDecimal().convert()
    Out[]: converted_list = ['111223.22']

    """

    def __init__(self, to_float=False):
        
        self.other_input = {
            Decimal: self.decode_dec
        }
        
        self.to_float = to_float

    def decode_dec(self, decimal_obj):
        """
        Converts a Decimal object to a 

        """
        if self.to_float:
            return(float(decimal_obj))
        else:
            return(str(decimal_obj))

class Deserializer(ConvertDecimal):
    """
    A helper class that deserializes json so that it can properly loaded into Mongo.

    Emulate's the `default` and `json_util` callback functions from `bson`

    Main features

    * converts unicode to `str`
    * converts Decimal objects to `str` or `float`
    * converts datetime to `str`
    
    """

    def __init__(self, **kwargs):
        
        super(Deserializer, self).__init__(**kwargs)

        self.other_input = {
            unicode: self.to_string,
            Decimal: self.decode_dec,
            datetime.datetime: self.decode_date,
        }


    def to_string(self, unicode_obj):
        """
        Converts a unicode obj to a string
        """
        return(str(unicode_obj))

    def decode_date(self, date_obj):
        return(datetime.datetime.strftime(date_obj, '%Y-%m-%d %H:%S'))
