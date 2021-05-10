from django.core.management.base import BaseCommand
from main.models import Coach


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Coaches to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Coaches to create')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')

        if prefix is None:
            prefix = 'Coach'

        for i in range(count):
            Coach.objects.create(first_name=f'{prefix} {i}', team_tactics='Attack')
            self.stdout.write(f'{prefix} {i} created')
