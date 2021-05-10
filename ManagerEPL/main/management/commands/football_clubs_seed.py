from django.core.management.base import BaseCommand
from main.models import FootballClub


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Football Clubs to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Football Clubs to create')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')

        if prefix is None:
            prefix = 'Football Club'

        for i in range(count):
            FootballClub.objects.create(title=f'Football Club {i}')
            self.stdout.write(f'{prefix} {i} created')
