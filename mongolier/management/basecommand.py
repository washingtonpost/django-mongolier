"""
basecommand.py

"""
from optparse import make_option

from django.core.management.base import BaseCommand
from mongolier import MongoConnection


class MongolierCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
    make_option('-d','--database',
        dest='database',
        default='test',
        help='MongoDB database name'),
    make_option('-c','--collection',
        dest='collection',
        default='test',
        help='MongoDB collection name'),
    make_option('-a','--auth',
        dest='auth',
        default=None,
        help='MongoDB auth'),
    make_option('-o','--respect_objectid',
        dest='respect_objectid',
        default=False,
        action='store_true',
        help='MongoDB database name')
    )
    def auth(self, **options):
        """
        Authorize with a database/collection
        """
        connection_object = MongoConnection(db=options['database'],
                                    collection=options['collection'],
                                    auth=options['auth'])

        return(connection_object.connect())