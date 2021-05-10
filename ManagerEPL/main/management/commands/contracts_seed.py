from django.core.management.base import BaseCommand
from main.models import Contract
from datetime import datetime, timedelta

now = datetime.now()
future = now + timedelta(days=730)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of Contracts to create')
        parser.add_argument('-p', '--prefix', type=str, help='Prefix for Contracts to create')

    def handle(self, *args, **options):
        count = options.get('count')
        prefix = options.get('prefix')

        if prefix is None:
            prefix = 'Contract'

        for i in range(count):
            Contract.objects.create(signing_date=now, expiration_date=future, salary=100000)
            self.stdout.write(f'{prefix} {i} created')
