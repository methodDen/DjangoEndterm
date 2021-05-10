import random
from django.core.management.base import BaseCommand
from main.models import Stadium


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Stadiums to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Stadiums to create')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')

        if prefix is None:
            prefix = 'Stadium'

        for i in range(count):
            Stadium.objects.create(name=f'Stadium {i}', capacity=random.randint(1500, 150000))
            self.stdout.write(f'{prefix} {i} created')
