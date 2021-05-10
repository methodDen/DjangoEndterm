from django.core.management.base import BaseCommand
from main.models import Stadium


class Command(BaseCommand):
    help = 'Management command to delete Stadiums'

    def add_arguments(self, parser):
        parser.add_argument('stadium_ids', nargs='+', type=int, help='Total number of Stadiums to delete')

    def handle(self, *args, **options):
        stadium_ids = options.get('stadium_ids')
        self.stdout.write(str(stadium_ids))

        for s_id in stadium_ids:
            try:
                stadium = Stadium.objects.get(id=s_id)
                stadium.delete()
                self.stdout.write(self.style.SUCCESS(f'Stadium with id {s_id} deleted'))
            except Stadium.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Stadium with id {s_id} does not exist'))
