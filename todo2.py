#!/bin/env python

import display # local module
import yaml
import re
import sys
from optparse import OptionParser, Option, OptionValueError
import time
from datetime import datetime, date, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import os.path as path
from copy import deepcopy

# Option Parsing
class MultipleOption(Option):
    ACTIONS = Option.ACTIONS + ("extend",)
    STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
    TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
    ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "extend":
            values.ensure_value(dest, []).append(value)
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)

parser = OptionParser(option_class=MultipleOption, usage="usage: %prog [todo_file] [options]")
parser.add_option('-t', '--todo', dest="new_tasks", action="extend", metavar="ITEM", help="new item to add to todo list")
parser.add_option('-d', '--display', dest="show_tasks", action="store_true", help="list items on the todo list")
parser.add_option('-s', '--status', dest="status", help="update or select a status")
parser.add_option('-j', '--job', dest="job", type="string", help="job to do something with")
parser.add_option('-c', '--closes-job', dest="job_closed", action="store_true", help="status update closes the todo list item (use with -s)")
parser.add_option('-a', '--show-all', dest="show_all", action="store_true", help="Whether to show all tasks, or only the pending ones")
parser.add_option('-r', '--remove', dest="remove", action="store_true", help="remove the selected job or status")
parser.add_option('', '--add-repeat', dest="new_repeat", help='create a repeat (use format "name (<n>-<year|month|week|day|hour|minute>[, ...])")')
parser.add_option('-l', '--list-repeats', dest="list_repeats", action="store_true", help='show a list of current repeats to use in scheduling')
parser.add_option('-S', '--schedule-job', dest="job_schedule", help='schedule a "start_date (repeat name)" for a -j')
parser.add_option('', '--log', dest="log_distance", metavar="DAYS", help="show the last DAYS worth of statuses")
parser.add_option('', '--short', dest="short_output", action="store_true", help="Dump a simple output consisting of just the tasks")
parser.add_option('', '--pm', dest="pm_only", action="store_true", help="When combined with --log, show only completed repeating tasks (preventative maintenance)")

(options, args) = parser.parse_args()

# process job flag
if options.job != None:
    try:
        options.job = [int(x) for x in options.job.split(',')]
    except (e):
        print "Invalid -j syntax, should be <int>[,<int>[,<int>...]]"
        options.job = None

# configuration
if len(args) > 0:
    dataFileName = args[0]
else:
    dataFileName = path.join(path.expanduser('~'), 'todo.py.yaml')

INVALID_JOB_MESSAGE = "Invalid job id, the ID is in parenthesis to the left of a job when you run this script with -d"
INVALID_JOB_SCHEDULE_FORMAT = "Invalid job schedule format.  See help for -S"

# functions
def task_closed(task):
    stat = last_status(task)
    return stat['closes'] if stat and 'closes' in stat else False
def task_repeats(task):
    if not 'schedules' in task: return False
    ok = False
    for schedule in task['schedules']:
        if 'repeat' in schedule:
            for field in ['week', 'month', 'year', 'day']:
                if field in schedule['repeat'] and schedule['repeat'][field] > 0: ok = True
    return ok
def last_status(task):
    if 'statuses' in task and task['statuses']:
        return max(task['statuses'], key=lambda x: x['dt'])
    else:
        return None
def task_short_name(task_id):
    return storeData['tasks'][task_id]['t'][:64] + ('...' if len(storeData['tasks'][task_id]['t']) > 64 else "")
def repeat_description(repeat):
    ret = ''
    fields = ['minute', 'hour', 'day', 'week', 'month', 'year']
    started = False
    lastUsed = -1
    for field in fields:
        if field not in repeat:
            continue
        if repeat[field] == 0:
            if not started:
                ret += "on "
                started = True
            ret += 'the same %s of ' % field
            lastUsed = 0
        elif repeat[field] > 0:
            if lastUsed == 0:
                ret += 'the %s ' % field
            ret += 'every %s%s%s from ' % (str(repeat[field]) + ' ' if repeat[field] > 1 else '', field, 's' if repeat[field] > 1 else '')
            started = True
            lastUsed = 1
    return ret + "the start date"
def repeat_list(task):
    if not 'schedules' in task: return ''
    ret = ''
    for schedule in task['schedules']:
        if 'repeat' in schedule:
            if len(ret) > 0: ret += ", "
            ret += schedule['repeat']['name']
    return ret
def preprocess_data(storeData):
    changedData = False
    if 'tasks' not in storeData:
        storeData['tasks'] = []
    if 'repeat_assignment' in storeData:
        new_repeat_assignment = {}
        for repeat in storeData['repeat_assignment']:
            ro = None
            for r in storeData['repeats']:
                if r['name'] == repeat:
                    ro = r
                    break
            if ro:
                for task in storeData['repeat_assignment'][repeat]:
                    t = {'t': task['t'], 'dt': datetime.now(), 'schedules': [{'repeat': ro, 'start_dt': (parse(str(task['d'])) if type(task['d']) != datetime else task['d']) if 'd' in task and task['d'] != None else datetime.now()}]}
                    if 's' in task:
                        for s in task['s']:
                            if 'dt' in s and type(s['dt']) != datetime:
                                if s['dt'] == 'now':
                                    s['dt'] = datetime.now()
                                else:
                                    s['dt'] = parse(str(s['dt']))
                        t['statuses'] = task['s']
                    storeData['tasks'].insert(0, t)
            else:
                print "Skipped values for repeat ('%s') because it wasn't in the repeats list" % repeat
                new_repeat_assignment[repeat] = storeData['repeat_assignment']
        storeData['repeat_assignment'] = new_repeat_assignment
        changedData = True
    for task in storeData['tasks']: # open any closed jobs that are due again
        if 'statuses' in task:
            for status in task['statuses']:
                if 'dt' not in status or status['dt'] == 'now':
                    status['dt'] = datetime.now()
                elif type(status['dt']) != datetime:
                    status['dt'] = parse(str(status['dt']))
        if type(task) == str:
            i = storeData['tasks'].index(task)
            task = storeData['tasks'][i] = {'t': task, 'dt': datetime.now()}
            changedData = True
        if 'dt' not in task:
            task['dt'] = datetime.now()
            changedData = True
        elif type(task['dt']) == date:
            task['dt'] = datetime.combine(task['dt'], datetime.min.time())
            changedData = True
        elif type(task['dt']) != datetime:
            task['dt'] = datetime.now()
            changedData = True
        if 'schedules' in task and task['schedules'] != None and task_closed(task):
            for schedule in task['schedules']:
                r = schedule['repeat']
                # now for the tricky part... finding the last time the task should have been done
                if 'start_dt' not in schedule:
                    last = deepcopy(task['dt'])
                else:
                    last = deepcopy(schedule['start_dt'])
                if type(last) == date:
                    last = datetime.combine(last, datetime.min.time())
                start = deepcopy(last)
                last_unit = 'start'
                if 'year' in r and type(r['year']) == int and r['year'] > 0:
                    yearsToNow = relativedelta(datetime.now(), last).years
                    last += relativedelta(years=yearsToNow - yearsToNow % r['year'])
                    last_unit = 'year'
                if 'month' in r:
                    if type(r['month']) == int and r['month'] > 0:
                        monthsToNow = relativedelta(datetime.now(), last).months
                        last += relativedelta(months=monthsToNow - monthsToNow % r['month'])
                    last_unit = 'month'
                if 'week' in r:
                    if type(r['week']) == int and r['week'] > 0:
                        weeksToNow = (datetime.now()-last).days/7
                        last += relativedelta(weeks=weeksToNow - weeksToNow % r['week'])
                    elif last_unit == 'year':
                        last += relativedelta(weeks=last.isocalendar()[1]-start.isocalendar()[1])
                    last_unit = 'week'
                if 'day' in r:
                    if type(r['day']) == int and r['day'] > 0:
                        daysToNow = (datetime.now()-last).days # relativedelta(datetime.now(), last).days
                        last += relativedelta(days=daysToNow - daysToNow %r['day'])
                    else:
                        if last_unit == 'week':
                            last += relativedelta(days=start.weekday()-last.weekday())
                if 'hour' in r and type(r['hour']) == int and r['hour'] > 0:
                    hoursToNow = relativedelta(datetime.now(), last).hours
                    last += relativedelta(hours=hoursToNow - hoursToNow %r['hour'])
                if 'minute' in r and type(r['minute']) == int and r['minute'] > 0:
                    minutesToNow = relativedelta(datetime.now(), last).minutes
                    last += relativedelta(minutes=minutesToNow - minutesToNow %r['minute'])
                if last > last_status(task)['dt'] and last <= datetime.now():
                    task['statuses'].insert(0, {'status': 'due to be done (for the "%s" schedule)' % r['name'], 'dt': datetime.now(), 'auto': True})
                    task['statuses'][0]['debug'] = '%s %s' % (last, last_status(task)['dt'])
                    changedData = True
    return changedData

# main
def main(storeData):
    usedOptions = False
    changedData = False
    # new task
    if options.new_tasks:
        if 'tasks' not in storeData:
            storeData['tasks'] = []
        for task in options.new_tasks:
            storeData['tasks'].append({"t": task, "dt": datetime.now()})
            print "Added (%s) as job id %d" % (task, len(storeData['tasks'])-1)
            changedData = True
        usedOptions = True
    # remove task
    if options.remove:
        if 'tasks' not in storeData:
            print "No tasks to delete!"
        elif options.job != None:
            for job in options.job:
                if job < len(storeData['tasks']):
                    if options.status:
                        if options.status.isdigit():
                            if 'statuses' in storeData['tasks'][job] and storeData['tasks'][job]['statuses']:
                                del storeData['tasks'][job]['statuses'][int(options.status)]
                                changedData = True
                            else:
                                print "No statuses to delete!"
                        else:
                            print "With -r, -s must give a numeric ID of a status, other value given"
                    else:
                        print 'Are you sure you want to delete task %d: "%s"?' % (job, task_short_name(job))
                        if raw_input().lower() in ['yes', 'y', 'sure', 'ok', '1']:
                            del storeData['tasks'][job]
                            print "Successfully deleted job %d!" % job
                            changedData = True
                        else:
                            print "Held off.  Didn't delete job."
                else:
                    print INVALID_JOB_MESSAGE
        else:
            print "You must specify which job you're talking about with -j"
        usedOptions = True
    # update status of, or close, job
    elif options.status or options.job_closed:
        if options.job != None:
            if 'tasks' not in storeData:
                print "You must enter some todo list items before updating a todo list item status"
            else:
                for job in options.job:
                    if job < len(storeData['tasks']):
                        if 'statuses' not in storeData['tasks'][job]:
                            storeData['tasks'][job]['statuses'] = []
                        storeData['tasks'][job]['statuses'].insert(0,{"status": options.status if options.status else 'closed', "dt": datetime.now(), "closes": options.job_closed if options.job_closed != None else False})
                        changedData = True
                    else:
                        print INVALID_JOB_MESSAGE
        else:
            print "(-s) You must specify what job you're talking about with -j"
        usedOptions = True
    # schedule a job
    if options.job_schedule:
        if options.job != None:
            if 'tasks' not in storeData or not storeData['tasks']:
                print "No tasks to schedule!"
            else:
                for job in options.job:
                    if job < len(storeData['tasks']):
                        if 'repeats' in storeData and storeData['repeats']:
                            m = re.match('(.*)\s*\(([^\)]+)\)$', options.job_schedule)
                            if not m:
                                print INVALID_JOB_SCHEDULE_FORMAT
                            else:
                                dt = parse(m.group(1)) if len(m.group(1)) > 0 else None
                                if m.group(2) not in [x['name'] for x in storeData['repeats']]:
                                    print "Invalid repeat specifier '%s'. Use -l to list options." % m.group(2)
                                else:
                                    if 'schedules' not in storeData['tasks'][job]:
                                        storeData['tasks'][job]['schedules'] = []
                                    repeat = None
                                    for r in storeData['repeats']:
                                        if r['name'] == m.group(2):
                                            repeat = r
                                            break
                                    record = {'repeat': repeat}
                                    if dt:
                                        record['start_dt'] = dt
                                    storeData['tasks'][job]['schedules'].append(record)
                                    changedData = True
                        else:
                            print "You can't specify a job's repetition without specifying any repeats!  Add one first."
                    else:
                        print INVALID_JOB_MESSAGE
        else:
            print "(-S) You must specify what job you want to schedule with -j"
        usedOptions = True
    # create repeat
    if options.new_repeat:
        if 'repeats' not in storeData:
            storeData['repeats'] = []
        m = re.match('(.+)\s+\(([a-z0-9,\- ]+)\)$', options.new_repeat)
        if m == None:
            print "Invalid repeat specification (see help for --add-repeat)"
        else:
            record = {x.split('-')[1]:int(x.split('-')[0]) for x in m.group(2).split(',')}
            record['name'] = m.group(1)
            storeData['repeats'].append(record)
            changedData = True
        usedOptions = True
    # show repeats
    if options.list_repeats:
        print "Repeats:"
        if 'repeats' in storeData and storeData['repeats']:
            for repeat in storeData['repeats']:
                print '"%s" (%s)' % (repeat['name'], repeat_description(repeat))
        else:
            print "No repeats to list!"
        usedOptions = True
    # show statuses log
    if options.log_distance:
        statusCount = 0
        print "Past statuses:"
        for task in storeData['tasks']:
            if 'statuses' in task and len(task['statuses']) > 0 and ((not options.pm_only) or task_repeats(task)):
                list = "\t\t" if options.pm_only else ""
                allEvents = []
                statusIndex = 1
                for status in task['statuses']:
                    if status['dt'] > (datetime.now()-relativedelta(days=int(options.log_distance))) and ((not options.pm_only) or ('closes' in status and status['closes'] == True)):
                        if options.pm_only:
                            list += "{0:%m-%d-%y},  ".format(status['dt'])
                            if (statusIndex % 6 == 0): list += "\n\t\t"
                            statusIndex += 1
                            allEvents.append(status['dt'])
                        else:
                            list += "\t\t(%s) %s\n" % (str(status['dt']), status['status'] if 'status' in status else ('done' if 'closes' in status and status['closes'] == True else ''))
                        statusCount += 1
                if list != "":
                    print "\t%s (%s)" % (task['t'].replace('\n', '\n\t'), repeat_list(task))
                    print list[0:-1]
                    allEvents.append(datetime.now())
                    if options.pm_only: display.aDate(allEvents)
        print "%d things done in the last %s days." % (statusCount, options.log_distance)
        usedOptions = True
    # show jobs
    if not usedOptions or options.show_tasks or options.short_output:
        if 'tasks' not in storeData:
            print 'No tasks to show!'
        else:
            # show specific job
            if options.job != None:
                for job in options.job:
                    if job < len(storeData['tasks']):
                        # show job name
                        print 'Task %d: "%s":' % (job, task_short_name(job))
                        
                        # show repeats
                        if 'schedules' in storeData['tasks'][job]:
                            print "- Schedules:"
                            for schedule in storeData['tasks'][job]['schedules']:
                                print '    ' + repeat_description(schedule['repeat'])
                        
                        # show statuses
                        if 'statuses' in storeData['tasks'][job]:
                            storeData['tasks'][job]['statuses'] = sorted(storeData['tasks'][job]['statuses'], key=lambda x: x['dt'], reverse=True)
                            print "- Events:"
                            for status in storeData['tasks'][job]['statuses']:
                                print "    ({1}) ({0:%m/%d/%y %I:%M%p}) {3} {2}".format(status['dt'], storeData['tasks'][job]['statuses'].index(status), status['status'] if 'status' in status else '', '*' if 'closes' in status and status['closes'] else ' ')
                            changedData = True # make sure our order gets saved, because we like it
                        else:
                            print "No statuses to show for that job!"
                    else:
                        print INVALID_JOB_MESSAGE
            # show all jobs
            else:
                print "Tasks as of %s:" % str(date.today())
                # sort tasks
                def taskCmp(left, right):
                    if task_closed(left)-task_closed(right) == 0:
                        if task_closed(left):
                            return 0
                        elif ('schedules' in left)-('schedules' in right) == 0:
                            if 'schedules' in left:
                                if (last_status(left) != None) - (last_status(right) != None) == 0:
                                    if last_status(left) != None:
                                        return int((last_status(right)['dt']-last_status(left)['dt']).total_seconds())
                                    else:
                                        return int((left['dt']-right['dt']).total_seconds())
                                else:
                                    return (last_status(left) != None) - (last_status(right) != None)
                            else:
                                return int((right['dt']-left['dt']).total_seconds())
                        else:
                            return ('schedules' in left)-('schedules' in right)
                    else:
                        return task_closed(left)-task_closed(right)
                sortedTasks = sorted(storeData['tasks'], cmp=taskCmp, reverse=True)
                for task in sortedTasks:
                    if not options.show_all and task_closed(task):
                        continue
                    l = last_status(task)
                    repeats = '(one-time)'
                    if l == None and 'schedules' in task:
                        repeats = '(done '
                        for schedule in task['schedules']:
                            repeats += schedule['repeat']['name'] + ","
                        repeats = repeats[:-1] + ')'
                    if options.short_output:
                        print task['t'].replace('\n', '\n\t')
                    else:
                        print "({1: >3}) ({0:%m/%d/%y}) {3} {2}".format(last_status(task)['dt'] if last_status(task) else task['dt'], storeData['tasks'].index(task), task['t'], '*' if task_closed(task) else ' '), "({0} -- {1:%m/%d/%y})".format(l['status'] if 'status' in l else '', l['dt']) if l != None else repeats
    return changedData

# execution start
if not path.exists(dataFileName):
    print "File %s doesn't exist. Create it?" % dataFileName
    sys.stdout.flush()
    if raw_input().lower() in ['yes', 'y', 'sure', 'ok', '1']:
        open(dataFileName, 'a').close()
        print "File created!"
    else:
        print "No valid file to read from/write to. Quiting"
        sys.exit()
inf = open(dataFileName, 'r')
storeData = yaml.load(inf)
inf.close()
if storeData == None:
    storeData = {}

changedData = preprocess_data(storeData)
if main(storeData) or changedData: # Whether or not it did anything with the data
    outf = open(dataFileName, 'w')
    outf.write(yaml.dump(storeData, default_flow_style=False, indent=4))
    outf.close()
