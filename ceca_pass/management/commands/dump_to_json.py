# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ceca_pass.helpers import dump_to_json


class Command(BaseCommand):
    help = """
            Dumps the information to a json file
        """

    def handle(self, *args, **options):
        dump_to_json()
