from django.core.management.base import BaseCommand
from main.models import Contract


class Command(BaseCommand):
    help = 'Management command to delete Contracts'
    def add_arguments(self, parser):
        parser.add_argument('contract_ids', nargs = '+', type=int, help='Total number of Contracts to delete')


    def handle(self, *args, **options):
        contract_ids = options.get('contract_ids')
        self.stdout.write(str(contract_ids))

        for c_id in contract_ids:
            try:
                contract = Contract.objects.get(id=c_id)
                contract.delete()
                self.stdout.write(self.style.SUCCESS(f'Contract with id {c_id} deleted'))
            except Contract.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Contract with id {c_id} does not exist'))

