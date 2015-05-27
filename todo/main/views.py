
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from main.models import Task, Repeat, Schedule, Status
from main.forms import RepeatForm, ScheduleForm, TaskForm, StatusFormBasic
from django.utils.html import strip_tags
from datetime import datetime

# Create your views here.

# TODO: delete this
def genericModViewNoForm(request, t, context, typeName, foreign={}):
    if request.method == 'POST':
        data = request.POST
        obj = None
        if 'id' in data and data['id'] != '':
            if not data['id'].isdigit():
                return HttpResponse("Invalid task id, must be a number")
            obj = t.objects.get(pk=int(data['id']))
        else:
            obj = t()
        if 'debug' not in context: context['debug'] = ''
        for key, value in request.POST.iteritems():
            if hasattr(obj, key) and value != '':
                context['debug'] += key + ": " + value + "<br>"
                setattr(obj, key, value)
        obj.save()
        if 'closeafter' in data:
            return redirect(typeName + 's/list.html')
        context[typeName] = obj
    if request.GET and 'id' in request.GET and request.GET['id'].isdigit():
        context[typeName] = t.objects.get(pk=int(request.GET['id']))
    return render(request, typeName + 's/modify.html', context)

def genericModView(request, obj_class, form_class, template, context={}):
    instance = None
    if request.GET and 'id' in request.GET and request.GET['id'].isdigit():
        instance = obj_class.objects.get(pk=request.GET['id'])
    elif request.POST and 'id' in request.POST and request.POST['id'].isdigit():
        instance = obj_class.objects.get(pk=request.POST['id'])
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
        if 'closeafter' in request.POST:
            return redirect('list.html')
    else:
        form = form_class(instance=instance)
    context['form'] = form.as_p()
    context['obj'] = instance
    return render(request, template, context)

def genericListView(request, t, context, typeName):
    if request.method == "GET":
        data = request.GET
        if 'action' in data:
            if data['action'] == 'delete' and 'id' in data and data['id'].isdigit():
                t.objects.get(pk=data['id']).delete()
    context[typeName + '_list'] = t.objects.all()
    return render(request, typeName + 's/list.html', context)
    
def taskView(request):
    context = {}
    if request.POST and 'mod' in request.POST and request.POST['mod'] == 'stat':
        return HttpResponse(StatusFormBasic(request.POST).handleInput())

    context['all_schedules'] = Schedule.objects.all()
    # TODO: get rid of duplicate code below of genericModView
    instance = None
    if request.GET:
        if 'action' in request.GET:
            if request.GET['action'] == 'rmstat':
                try:
                    s = Status.objects.get(id=request.GET['id'])
                    s.delete()
                    return HttpResponse("OK")
                except ObjectDoesNotExist:
                    return HttpResponse("Invalid status id")
        if 'id' in request.GET and request.GET['id'].isdigit():
            instance = Task.objects.get(pk=request.GET['id'])
    elif request.POST and 'id' in request.POST and request.POST['id'].isdigit():
        instance = Task.objects.get(pk=request.POST['id'])
    context['statForm'] = StatusFormBasic(initial={'task':instance}).as_p()
    if (instance != None):
        context['statuses'] = instance.status_set.all().order_by('-date')
    return genericModView(request, Task, TaskForm, 'tasks/modify.html', context=context)

def taskList(request, showDue=False):
    context = {}
    if request.POST:
        return HttpResponse(StatusFormBasic(request.POST).handleInput())
    elif request.method == "GET":
        data = request.GET
        if 'action' in data:
            if data['action'] == 'delete' and 'id' in data and data['id'].isdigit():
                Task.objects.get(pk=data['id']).delete()
                return redirect("/tasks/")
    context['statForm'] = StatusFormBasic().as_p()
    if showDue:
        context['task_list'] = Task.objects.filter(next_date__lt=datetime.now()).order_by("next_date")
    else:
        context['task_list'] = Task.objects.all().order_by("next_date")
    return render(request, 'tasks/list.html', context)
    
def repeatView(request, repeat_id=None, action=None):
    context = {}
    instance = None
    if (repeat_id != None):
        instance = Repeat.objects.get(id=repeat_id)
    if (action == "delete"):
        if instance != None:
            instance.delete()
        return redirect('/repeats')
    if request.method == "POST":
        form = RepeatForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
        if 'closeafter' in request.POST:
            return redirect('../list.html')
    else:
        form = RepeatForm(instance=instance)
    if instance != None:
        context['task_list'] = Task.objects.filter(schedules__repeat=instance)
    else:
        context['task_lsit'] = []
    context['form'] = form.as_p()
    context['obj'] = instance
    return render(request, 'repeats/modify.html', context)

def repeatList(request):
    return genericListView(request, Repeat, {}, 'repeat')
    
def scheduleView(request):
    context = {}
    context['all_repeats'] = Repeat.objects.all()
    return genericModView(request, Schedule, ScheduleForm, 'schedules/modify.html', context)

def dueTaskList(request):
    return taskList(request, showDue=True)

def scheduleList(request):
    return genericListView(request, Schedule, {}, 'schedule')
    
def userView(request):
    return HttpResponse("List of tasks")

def raw(request):
    raw = ''
    tasks = Task.objects.all()
    for task in tasks:
        if task.schedules.count() == 0:
            continue
        raw += task.name + ' -- ' + ','.join([unicode(schedule) for schedule in task.schedules.all()]) + '<br>\n'
    return HttpResponse(raw)