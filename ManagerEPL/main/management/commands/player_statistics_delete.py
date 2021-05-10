from django.core.management.base import BaseCommand
from main.models import PlayerStatistics


class Command(BaseCommand):
    help = 'Management command to delete Player Statistics'

    def add_arguments(self, parser):
        parser.add_argument('player_statistics_ids', nargs='+', type=int,
                            help='Total number of Player Statistics to delete')

    def handle(self, *args, **options):
        player_statistics_ids = options.get('player_statistics_ids')
        self.stdout.write(str(player_statistics_ids))

        for ps_id in player_statistics_ids:
            try:
                player_statistics = PlayerStatistics.objects.get(id=ps_id)
                player_statistics.delete()
                self.stdout.write(self.style.SUCCESS(f'Player Statistics with id {ps_id} deleted'))
            except PlayerStatistics.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Player Statistics with id {ps_id} does not exist'))
