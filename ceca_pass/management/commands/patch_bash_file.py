# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ceca_pass.helpers import patch_bash_file


class Command(BaseCommand):
    help = """
            Patchs the bash file.
        """

    def handle(self, *args, **options):
        patch_bash_file()
