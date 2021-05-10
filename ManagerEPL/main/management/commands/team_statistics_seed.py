from django.core.management.base import BaseCommand
from main.models import TeamStatistics


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='''Total number of Team Statistics to create''')
        parser.add_argument('-p', '--prefix', type=str, help='''Prefix for Team Statistics to create''')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')

        if prefix is None:
            prefix = 'Team Statistics'

        for i in range(count):
            TeamStatistics.objects.create(matches_played=30, goals_scored=50, points=50, place=5)
            self.stdout.write(f'{prefix} {i} created')
