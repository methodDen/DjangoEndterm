from django.core.management.base import BaseCommand
from main.models import Player


class Command(BaseCommand):
    help = 'Management command to delete Players'
    def add_arguments(self, parser):
        parser.add_argument('player_ids', nargs = '+', type=int, help='Total number of Players to delete')


    def handle(self, *args, **options):
        player_ids = options.get('player_ids')
        self.stdout.write(str(player_ids))

        for p_id in player_ids:
            try:
                player = Player.objects.get(id=p_id)
                player.delete()
                self.stdout.write(self.style.SUCCESS(f'Player with id {p_id} deleted'))
            except Player.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Player with id {p_id} does not exist'))

