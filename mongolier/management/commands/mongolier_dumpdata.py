"""
mongolier_dumpdata.py

An emulation of Django's dumpdata command for MongoDB

Currently only supports being able to dump one collection at a time.
"""
from optparse import make_option
from django.core.management.base import CommandError
from mongolier.utils.fixtures import CreateFixture
from mongolier.management.basecommand import MongolierCommand

class Command(MongolierCommand):
    option_list = MongolierCommand.option_list
    def handle(self, *args, **options):

        mongo = self.auth(**options)

        fixture_creator = CreateFixture(mongo)

        fixture_creator.create()