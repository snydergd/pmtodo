from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from django.db import models


class Repeat(models.Model):
    # year of -1 means ignore year of dates
    # year of 0 means dates with same year
    # year of n>0 means dates in year and every nth year after
    name = models.CharField('e.g. monthly', max_length=200, default='')
    day = models.IntegerField(default=-1)
    week = models.IntegerField(default=-1)
    month = models.IntegerField(default=-1)
    year = models.IntegerField(default=-1)


class Schedule(models.Model):
    repeat = models.ForeignKey(Repeat)
    start_date = models.DateTimeField('Date from which to repeat')
    
    def __unicode__(self):
        # TODO: Describe when it occurs rather than start date
        #  e.g. every monday
        return self.repeat.name + ' from ' +self.start_date.strftime('%b %dst, %Y')


class Task(models.Model):
    name = models.CharField('Name of task', max_length=200)
    desc = models.CharField('What is involved', max_length=300)
    date_created = models.DateTimeField('Date created', default=datetime.now, blank=True)
    schedules = models.ManyToManyField(Schedule)

    def nextScheduledTime(self):
        schedules = Schedule.objects.get(task__pk=self.pk)
        next_occurance = datetime.min
        for schedule in schedules:
            last = schedule.start_date
            r = schedule.repeat
            last_unit = 'start'
            
            if r.year > 0:
                years_to_now = relativedelta(datetime.now(), last).years
                last += relativedelta(years=years_to_now - years_to_now % r.year)
                last_unit = 'year'
            if r.month > -1:
                if r.month > 0:
                    months_to_now = relativedelta(datetime.now(), last).months
                    last += relativedelta(months=months_to_now - months_to_now % r.month)
                last_unit = 'month'
            if r.week > -1:
                if r.week > 0:
                    weeks_to_now = (datetime.now()-last).days/7
                    last += relativedelta(weeks=weeks_to_now - weeks_to_now % r.week)
                elif last_unit == 'year':
                    last += relativedelta(weeks=last.isocalendar()[1]-start.isocalendar()[1])
                last_unit = 'week'
            if r.day > -1:
                if r.day > 0:
                    days_to_now = (datetime.now()-last).days # relativedelta(datetime.now(), last).days
                    last += relativedelta(days=days_to_now - days_to_now % r.day)
                else:
                    if last_unit == 'week':
                        last += relativedelta(days=start.weekday()-last.weekday())
            if last < next_occurance:
                next_occurance = last
        return next_occurance


class Status(models.Model):
    task = models.ForeignKey(Task)
