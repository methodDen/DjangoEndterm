from django.core.management.base import BaseCommand
from main.models import TeamStatistics


class Command(BaseCommand):
    help = 'Management command to delete Team Statistics'

    def add_arguments(self, parser):
        parser.add_argument('team_statistics_ids', nargs='+', type=int,
                            help='''Total number of Team Statistics to delete''')

    def handle(self, *args, **options):
        team_statistics_ids = options.get('team_statistics_ids')
        self.stdout.write(str(team_statistics_ids))

        for ts_id in team_statistics_ids:
            try:
                team_statistics = TeamStatistics.objects.get(id=ts_id)
                team_statistics.delete()
                self.stdout.write(self.style.SUCCESS(f'Team Statistics with id {ts_id} deleted'))
            except TeamStatistics.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Team Statistics with id {ts_id} does not exist'))
