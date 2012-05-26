"""
mongolier_loaddata.py

An emulation of Django's loaddata command for MongoDB

"""
from optparse import make_option
from django.core.management.base import CommandError
from mongolier.utils.fixtures import LoadFixture
from mongolier.management.basecommand import MongolierCommand

class Command(MongolierCommand):
    option_list = MongolierCommand.option_list
    help = "Load a json fixture into Mongo"
    args = "d <database> c <collection> a <auth> fixture_location"
    def handle(self, *args, **options):

        mongo = self.auth(**options)

        fixture_creator = LoadFixture(mongo)

        fixture_creator.load(args[0])