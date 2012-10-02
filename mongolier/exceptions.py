class IncorrectParameters(Exception):
    """
    Incorrect parameters were passed here.
    """


class ValueNotSupported(Exception):
    """
    Not a supported Value.
    """


class DoesNotExist(Exception):
    """
    Object or Value does not exist.
    """


class InvalidMode(Exception):
    """
    The mode set does not match the mode requested.
    """
