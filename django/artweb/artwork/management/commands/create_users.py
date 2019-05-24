# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from artwork.create_users import create_users


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_users()
