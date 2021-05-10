from django.core.management.base import BaseCommand
from main.models import Agent


class Command(BaseCommand):
    help = 'Management command to delete Agents'

    def add_arguments(self, parser):
        parser.add_argument('agent_ids', nargs='+', type=int, help='Total number of Agents to delete')

    def handle(self, *args, **options):
        agent_ids = options.get('agent_ids')
        self.stdout.write(str(agent_ids))

        for a_id in agent_ids:
            try:
                agent = Agent.objects.get(id=a_id)
                agent.delete()
                self.stdout.write(self.style.SUCCESS(f'Agent with id {a_id} deleted'))
            except Agent.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Agent with id {a_id} does not exist'))
