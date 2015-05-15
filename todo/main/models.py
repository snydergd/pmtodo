from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from math import ceil
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
        r = self.repeat
        s = ''
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        def ord(n):
            a = n % 10
            x = 'th'
            if a == 1: x = 'st'
            if a == 2: x = 'nd'
            if a == 3: x = 'rd'
            return str(n) + x
        if r.day == 0:
            if r.week == 0:
                d = int(ceil(self.start_date.day/7.0))
                if d == 0: d = 1
                s += '%s %s ' % (ord(d), weekdays[(self.start_date.weekday()+1)%7])
            elif r.week > 0:
                if r.week == 1:
                    s += "%s every week" % weekdays[self.start_date.weekday()]
                else:
                    s += "%s every %d weeks" % (weekdays[self.start_date.weekday()], r.week)
            else:
                s += ord(self.start_date.day) + ' day'
        else:
            if r.day > 0:
                s += 'every %d days of' % r.day
            else:
#                s += 'all of'
                pass
            if r.week == 0:
                s += ' the %s week' % ord(ceil(self.start_date.day/7.0))
            elif r.week > 0:
                s += ' every %d weeks' % r.week
        if r.month == 0:
            s += ' of ' + months[self.start_date.month-1]
        elif r.month > 0:
            s += ' of '
            if 12 % r.month == 0:
                if r.month == 1:
                    s += 'the month'
                else:
                    for i in range(self.start_date.month-1, self.start_date.month+11, r.month):
                        s += months[i%12] + ','
                    s = s[:-1]
            else:
                s += 'every %d months' % r.month
        if r.year == 0:
            s += ' of ' + str(self.start_date.year)
        elif r.year > 0:
            if r.year == 0:
                s += ' the year'
            elif r.year == 1:
                s += ' every year'
            else:
                s += ' of every %d years' % r.year
        s += ' starting ' + self.start_date.strftime('%Y-%m-%d')
        return s


class Task(models.Model):
    name = models.CharField('Name of task', max_length=200)
    desc = models.TextField('What is involved', blank=True, default='')
    date_created = models.DateTimeField('Date created', default=timezone.now, blank=True)
    schedules = models.ManyToManyField(Schedule, blank=True)
    next_date = models.DateTimeField('Cached date of next occurance', default=timezone.now, blank=True)
    
    def last_done(self):
        completions = self.status_set.filter(complete=True).order_by('-date')
        if completions.count() > 0:
            return completions[0].date
        else:
            return self.date_created
    
    def repeat_list_str(self):
        str = ''
        reps = Repeat.objects.filter(schedule__task=self).distinct()
        if reps.count() == 0:
            return None
        for repeat in reps:
            str += repeat.name + ','
        str = str[:-1]
        return str

    def next_scheduled_time(self):
        completions = self.status_set.filter(complete=True).order_by('-date')
        if completions.count() > 0:
            after = completions[0].date
        else:
            after = self.date_created
        return self.next_occurance_after(after)

    def next_occurance_after(self, after):
        schedules = self.schedules.all()
        next_occurance = timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
        if after == self.date_created and schedules.count() == 0:
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
                    # relativedelta.months here doesn't account for several years between
                    months_to_now = (after.year-last.year)*12 + (after.month-last.month)
                    # account for when the months of the dates is 1 apart, but dates are more than a month apart
                    if after.day-last.day > monthrange(last.year, last.month)[1]:
                        months_to_now += 1
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
                    next += relativedelta(weeks=next.isocalendar()[1]-schedule.start_date.isocalendar()[1])
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
                        diff = schedule.start_date.weekday()-last.weekday()
                        last += relativedelta(days=diff)
                        diff = schedule.start_date.weekday()-next.weekday()
                        next += relativedelta(days=diff)
            if next == None: next = next_occurance
            if next < next_occurance:
                next_occurance = next
        return next_occurance
    
    def __unicode__(self):
        return self.name


class Status(models.Model):
    task = models.ForeignKey(Task)
    text = models.TextField('What happened', blank=True, default='')
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
