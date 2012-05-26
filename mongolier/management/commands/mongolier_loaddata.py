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
    
    def handle(self, *args, **options):

        mongo = self.auth()

        fixture_creator = LoadFixture(mongo)

        fixture_creator.load(args[0])