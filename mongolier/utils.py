"""
utils.py

Contains utilities and tools for pymongo
"""
from decimal import Decimal, getcontext

class ConvertDecimal(object):
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
        
        self.to_float = to_float
    
    def _decode_dict(self, input_dict):
        output = {}

        for key, item in input_dict.items():
            if isinstance(item, list):
                item = self._decode_list(item)

            if isinstance(item, dict):
                item = self._decode_dict(item)

            if isinstance(item, Decimal):
                item = self._decode_dec(item)

            output[key] = item
        return(output)

    def _decode_list(self, input_list):
        
        output = []

        for item in input_list:
            if isinstance(item, list):
                item = self._decode_list(item)

            if isinstance(item, dict):
                item = self._decode_dict(item)

            if isinstance(item, Decimal):
                item = self._decode_dec(item)

            output.append(item)
        return(output)

    def _decode_dec(self, decimal_obj):
        
        if self.to_float:
            return(float(decimal_obj))
        else:
            return(str(decimal_obj))            

    def convert(self, iterable):
        """
        Convert
        """

        if isinstance(iterable, list):
            output = self._decode_list(iterable)

        if isinstance(iterable, dict):
            output = self._decode_dict(iterable)

        return(output)
