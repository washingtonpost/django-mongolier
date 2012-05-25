"""
basecommand.py

"""
from optparse import make_option

from django.core.management.base import BaseCommand
from mongolier import MongoConnection


class MongolierCommand(BaseCommand):
    help = "An emulation of Django's dumpdata."
    option_list = BaseCommand.option_list + (
        make_option('-d','--database',
            dest='database',
            default='test',
            help='MongoDB database name'),
        ),
        make_option('-c','--collection',
            dest='collection',
            default='test',
            help='MongoDB collection name'),
        ),
        make_option('-a','--auth',
            dest='auth',
            default=None,
            help='MongoDB auth'),
        ),
        make_option('-o','--respect_objectid',
            dest='respect_objectid',
            default=False,
            help='MongoDB database name'),
        )
    
    def _auth(self):

        connection_object = MongoConnection(database=options['database'],
                                    collection=options['collection'].
                                    auth=options['auth'])

        return(connection_object.connect())