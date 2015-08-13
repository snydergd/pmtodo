from django.core.management.base import BaseCommand, CommandError
from main.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = 'Take recalculate the next_occurance fields of all tasks'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for task in Task.objects.all():
            task.next_occurance = task.next_scheduled_time()
            try:
                task.next_due = task.next_occurance_after(task.next_date+timedelta(days=1))
            except OverflowError:
                task.next_due = task.next_date
            task.save()

#            raise CommandError('Poll "%s" does not exist' % poll_id)

#            self.stdout.write('Successfully closed poll "%s"' % poll_id)