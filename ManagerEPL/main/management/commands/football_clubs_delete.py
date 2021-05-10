from django.core.management.base import BaseCommand
from main.models import FootballClub


class Command(BaseCommand):
    help = 'Management command to delete Football Clubs'

    def add_arguments(self, parser):
        parser.add_argument('football_club_ids', nargs='+', type=int, help='Total number of Football Clubs to delete')

    def handle(self, *args, **options):
        football_club_ids = options.get('football_club_ids')
        self.stdout.write(str(football_club_ids))

        for fc_id in football_club_ids:
            try:
                football_club = FootballClub.objects.get(id=fc_id)
                football_club.delete()
                self.stdout.write(self.style.SUCCESS(f'Football Club with id {fc_id} deleted'))
            except FootballClub.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Football Club with id {fc_id} does not exist'))
