from django.core.management.base import BaseCommand
from main.models import PlayerStatistics


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='''Total number of Player Statistics to create''')
        parser.add_argument('-p', '--prefix', type=str, help='''Prefix for Player Statistics to create''')
        parser.add_argument('-i', '--injured', action='store_true', help='''Create Player Statistics with injury''')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')
        injured = options.get('injured')

        if prefix is None:
            prefix = 'Player Statistics'

        for i in range(count):
            if injured:
                PlayerStatistics.objects.create(matches_played=30, goals_scored=10, is_injured=True)
            else:
                PlayerStatistics.objects.create(matches_played=30, goals_scored=10, is_injured=False)
            self.stdout.write(f'{prefix} {i} created')
