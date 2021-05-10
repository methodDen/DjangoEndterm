from django.core.management.base import BaseCommand
from main.models import Match


class Command(BaseCommand):
    help = 'Management command to delete Matches'
    def add_arguments(self, parser):
        parser.add_argument('match_ids', nargs = '+', type=int, help='Total number of Matches to delete')


    def handle(self, *args, **options):
        match_ids = options.get('match_ids')
        self.stdout.write(str(match_ids))

        for m_id in match_ids:
            try:
                match = Match.objects.get(id=m_id)
                match.delete()
                self.stdout.write(self.style.SUCCESS(f'Match with id {m_id} deleted'))
            except Match.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Match with id {m_id} does not exist'))

