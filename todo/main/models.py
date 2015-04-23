from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from copy import deepcopy

from django.utils import timezone

from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

class Repeat(models.Model):
    # year of -1 means ignore year of dates
    # year of 0 means dates with same year
    # year of n>0 means dates in year and every nth year after
    name = models.CharField('e.g. monthly', max_length=200, default='')
    day = models.IntegerField(default=-1)
    week = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    year = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.name

class Schedule(models.Model):
    repeat = models.ForeignKey(Repeat)
    start_date = models.DateTimeField('Date from which to repeat')
    
    def __unicode__(self):
        # TODO: Describe when it occurs rather than start date
        #  e.g. every monday
        return self.repeat.name + ' from ' +self.start_date.strftime('%b %dst, %Y')


class Task(models.Model):
    name = models.CharField('Name of task', max_length=200)
    desc = models.TextField('What is involved', max_length=300, blank=True)
    date_created = models.DateTimeField('Date created', default=timezone.now, blank=True)
    schedules = models.ManyToManyField(Schedule, blank=True)
    next_date = models.DateTimeField('Cached date of next occurance', default=timezone.now, blank=True)
    
    def last_done(self):
        completions = self.status_set.filter(complete=True).order_by('-date')
        if completions.count() > 0:
            return completions[0].date
        else:
            return self.date_created
    
    def next_scheduled_time(self):
        schedules = self.schedules.all()
        next_occurance = timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
        completions = self.status_set.filter(complete=True).order_by('-date')
        if completions.count() > 0:
            after = completions[0].date
        else:
            after = self.date_created
            if schedules.count() == 0:
                # if this task is on-time and hasn't been completed
                # then set next_occurance to creation date so it shows as incomplete
                next_occurance = self.date_created
        for schedule in schedules:
            last = deepcopy(schedule.start_date)
            r = schedule.repeat
            last_unit = 'start'
            next = None
            if r.year > 0:
                years_to_now = relativedelta(after, last).years
                last += relativedelta(years=years_to_now - years_to_now % r.year)
                last_unit = 'year'
                next = last + relativedelta(years=r.year)
            if r.month > -1:
                if r.month > 0:
                    months_to_now = relativedelta(after, last).months
                    last += relativedelta(months=months_to_now - months_to_now % r.month)
                    t = last + relativedelta(months=r.month)
                    if (next == None or t < next):
                        next = t
                last_unit = 'month'
            if r.week > -1:
                if r.week > 0:
                    weeks_to_now = (after-last).days/7
                    last += relativedelta(weeks=weeks_to_now - weeks_to_now % r.week)
                    t = last + relativedelta(weeks=r.week)
                    if (next == None or t < next):
                        next = t
                elif last_unit == 'year':
                    last += relativedelta(weeks=last.isocalendar()[1]-schedule.start_date.isocalendar()[1])
                last_unit = 'week'
            if r.day > -1:
                if r.day > 0:
                    days_to_now = (after-last).days # relativedelta(datetime.now(), last).days
                    last += relativedelta(days=days_to_now - days_to_now % r.day)
                    t = last + relativedelta(days=r.day)
                    if (next == None or t < next):
                        next = t
                else:
                    if last_unit == 'week':
                        diff = abs(schedule.start_date.weekday()-last.weekday())
                        if diff < 0 and int((last-diff)/7) < int(last/7):
                            diff += 7
                        last += relativedelta(days=diff)
            if next == None: next = next_occurance
            if next < next_occurance:
                next_occurance = next
        return next_occurance
    
    def __unicode__(self):
        return self.name


class Status(models.Model):
    task = models.ForeignKey(Task)
    text = models.CharField('What happened', max_length=1024)
    complete = models.BooleanField('Does it complete the task?', default=False)
    date = models.DateTimeField('Date of status', default=timezone.now, blank=True)


@receiver(m2m_changed, sender=Task.schedules.through)
@receiver(post_save, sender=Status)
@receiver(post_save, sender=Schedule)
def update_next_date(sender, **kwargs):
    if sender == Schedule:
        # update all statuses using this schedule
        tasks = kwargs['instance'].task_set.all()
    elif sender == Task.schedules.through:
        tasks = [kwargs['instance']]
        if not kwargs['action'] in ['post_add', 'post_remove', 'post_clear']:
            return
    else:
        tasks = [kwargs['instance'].task]
    for task in tasks:
        task.next_date = task.next_scheduled_time()
        task.save()
