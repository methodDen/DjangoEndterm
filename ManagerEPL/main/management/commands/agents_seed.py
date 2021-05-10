import random

from django.core.management.base import BaseCommand
from main.models import Agent


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Agents to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Agents to create')
        parser.add_argument('-e', '--experienced', action='store_true', help='Create experienced Agents')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')
        experienced = options.get('experienced')

        if prefix is None:
            prefix = 'Agent'

        for i in range(count):
            if experienced:
                Agent.objects.create(first_name=f'{prefix} {i}', age=random.randint(50, 70), contract_terms='Lorem ispum...')
            else:
                Agent.objects.create(first_name=f'{prefix} {i}', age=random.randint(17, 49), contract_terms='Lorem ipsum...')
            self.stdout.write(f'{prefix} {i} created')
