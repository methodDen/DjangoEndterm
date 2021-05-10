from django.core.management.base import BaseCommand
from main.models import Coach


class Command(BaseCommand):
    help = 'Management command to delete Coaches'
    def add_arguments(self, parser):
        parser.add_argument('coach_ids', nargs = '+', type=int, help='Total number of Coaches to delete')


    def handle(self, *args, **options):
        coach_ids = options.get('coach_ids')
        self.stdout.write(str(coach_ids))

        for c_id in coach_ids:
            try:
                coach = Coach.objects.get(id=c_id)
                coach.delete()
                self.stdout.write(self.style.SUCCESS(f'Coach with id {c_id} deleted'))
            except Coach.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Coach with id {c_id} does not exist'))

