# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ceca_pass.helpers import dump_to_bash


class Command(BaseCommand):
    help = """
            Dump all the passwords to a bash file
        """

    def handle(self, *args, **options):
        dump_to_bash()
