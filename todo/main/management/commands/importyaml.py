from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from main.models import Task, Schedule, Repeat, Status
from datetime import datetime, date
import yaml

class Command(BaseCommand):
    help = 'Imports a yaml file created with earlier todo2.py'

    def add_arguments(self, parser):
        parser.add_argument('in_file', nargs='*', type=open)

    def n_from_in(self, n):
        if type(n) != int:
            return 0
        return n
        
    def handle(self, *args, **options):
        for infile in options['in_file']:
            data = yaml.load(infile)
            infile.close()
            if 'repeats' in data:
                # TODO: handle non-array repeats value
                for r in data['repeats']:
                    new_r = Repeat()
                    if 'name' in r: new_r.name = r['name']
                    if 'year' in r: new_r.year = self.n_from_in(r['year'])
                    if 'month' in r: new_r.month = self.n_from_in(r['month'])
                    if 'week' in r: new_r.week = self.n_from_in(r['week'])
                    if 'day' in r: new_r.day = self.n_from_in(r['day'])
                    new_r.save()
                    r['new'] = new_r
            if 'tasks' in data:
                # TODO: handle non-array tasks
                for t in data['tasks']:
                    new_t = Task()
                    if 'dt' in t:
                        if type(t['dt']) == date:
                            t['dt'] = datetime.combine(t['dt'], datetime.min.time())                            
                        new_t.date_created = timezone.make_aware(t['dt'], timezone.get_default_timezone())
                    else:
                        new_t.date_created = timezone.now()
                    if 't' in t:
                        new_t.name = t['t']
                    new_t.save()
                    if 'schedules' in t:
                        # TODO: handle non-array schedules section
                        for s in t['schedules']:
                            new_s = Schedule()
                            if 'repeat' in s:
                                new_s.repeat = s['repeat']['new']
                            if 'start_dt' in s:
                                if type(s['start_dt']) == date:
                                    s['start_dt'] = datetime.combine(s['start_dt'], datetime.min.time())
                                new_s.start_date = timezone.make_aware(s['start_dt'], timezone.get_default_timezone())
                            else:
                                new_s.start_date = new_t.date_created
                            new_s.save()
                            new_t.schedules.add(new_s)
                    if 'statuses' in t:
                        # TODO: handle non-array status section
                        for s in t['statuses']:
                            new_s = Status()
                            if 'dt' in s:
                                if type(s['dt']) == date:
                                    s['dt'] = datetime.combine(s['dt'], datetime.min.time())
                                new_s.date = timezone.make_aware(s['dt'], timezone.get_default_timezone())
                            else:
                                new_s.date = new_t.date_created
                            if 'status' in s:
                                new_s.text = s['status']
                            if 'closes' in s:
                                new_s.complete = s['closes']
                            new_s.task = new_t
                            new_s.save()

#            raise CommandError('Poll "%s" does not exist' % poll_id)

#            self.stdout.write('Successfully closed poll "%s"' % poll_id)