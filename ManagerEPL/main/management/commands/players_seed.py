import random
from django.core.management.base import BaseCommand
from main.models import Player


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Players to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Players to create')
        parser.add_argument('-l', '--local', action='store_true', help='Create local Players')
        parser.add_argument('-f', '--foreign', action='store_true', help='Create foreign Players')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')
        local = options.get('local')
        foreign = options.get('foreign')

        if prefix is None:
            prefix = 'Player'

        for i in range(count):
            if local:
                Player.objects.create(first_name=f'{prefix} {i}', age=random.randint(18, 40), is_local=True)
            elif foreign:
                Player.objects.create(first_name=f'{prefix} {i}', age=random.randint(18, 40), is_foreign=True)
            else:
                Player.objects.create(first_name=f'{prefix} {i}', age=random.randint(18, 40))
            self.stdout.write(f'{prefix} {i} created')
