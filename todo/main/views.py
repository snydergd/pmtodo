
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from main.models import Task, Repeat, Schedule, Status
from main.forms import RepeatForm, ScheduleForm, TaskForm, StatusFormBasic
from django.utils.html import strip_tags
from datetime import datetime
from django.db.models import Q, Count
from django.utils import timezone

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
    if 'instance' in context:
        instance = context['instance']
    elif request.GET and 'id' in request.GET and request.GET['id'].isdigit():
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
    
def taskView(request, task_id=None, action=None):
    context = {}
    if request.POST and 'mod' in request.POST and request.POST['mod'] == 'stat':
        return HttpResponse(StatusFormBasic(request.POST).handleInput())
    if action == 'rmstat':
        try:
            s = Status.objects.get(id=request.GET['id'])
            s.delete()
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponse("Invalid status id")

    instance = None
    form = None
    if (task_id != None):
        context['instance'] = instance = Task.objects.get(id=task_id)
    if (action == "delete"):
        if instance != None:
            instance.delete()
        return redirect('/tasks')
    if request.method == "POST":
        form = TaskForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            if form.cleaned_data['repeat'] is not None and form.cleaned_data['start_date'] is not None:
                schedule = Schedule.objects.get_or_create(repeat=form.cleaned_data['repeat'], start_date=form.cleaned_data['start_date'])
                instance.schedules.add(schedule[0])
                form = TaskForm(instance=instance)
        if 'closeafter' in request.POST:
            return redirect('./')
    else:
        form = TaskForm(instance=instance)
    context['form'] = form.as_p()
    context['all_schedules'] = Schedule.objects.all()
    context['statForm'] = StatusFormBasic(initial={'task':instance}).as_p()
    context['obj'] = instance
    if (instance != None):
        context['statuses'] = instance.status_set.all().order_by('-date')
    return render(request, "tasks/modify.html", context)

def taskList(request, type=None):
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
    order_field = 'next_date'
    if (request.GET and 'order_by' in request.GET):
        order_field = request.GET['order_by']
    if type == "due":
        context['task_list'] = Task.objects.filter(next_date__lt=datetime.now()).order_by(order_field)
    else:
        context['task_list'] = Task.objects.all().order_by(order_field)
        """context['task_list_breakdown'] = (
        "One-time due: %d\nRepeating-due: %d" % 
        (context['task_list'].annotate(schedule_count=Count('schedules')).filter(Q(next_date__lt=timezone.now())
            & (Q(schedule_count=0)
                | (Q(schedule_count=1)
                    & Q(schedules__repeat__day=0)
                    & Q(schedules__repeat__month=0)
                    & Q(schedules__repeat__week=0)
                    & Q(schedules__repeat__year=0)))).count(),
          context['task_list'].filter(Q(next_date__lt=timezone.now()) & (Q(schedules__count__gt=1) | (Q(schedules__count=1) & Q(schedules__repeat__day__ne=0) | Q(schedules__repeat__month__ne=0) | Q(schedules__repeat__week__ne=0) | Q(schedules__repeat__year__ne=0)))).count()))"""
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
        context['task_list'] = Task.objects.filter(schedules__repeat=instance).distinct()
    else:
        context['task_list'] = []
    context['form'] = form.as_p()
    context['obj'] = instance
    return render(request, 'repeats/modify.html', context)

def repeatList(request):
    return genericListView(request, Repeat, {}, 'repeat')
    
def scheduleView(request):
    context = {}
    context['all_repeats'] = Repeat.objects.all()
    return genericModView(request, Schedule, ScheduleForm, 'schedules/modify.html', context)

def scheduleList(request):
    return genericListView(request, Schedule, {}, 'schedule')
    
def userView(request):
    return HttpResponse("List of tasks")

def statusList(request):
    context = {}
    context['statuses'] = Status.objects.all().order_by('-date')
    return render(request, 'statuses/list.html', context)
    
def raw(request):
    raw = ''
    tasks = Task.objects.all()
    for task in tasks:
        if task.schedules.count() == 0:
            continue
        raw += task.name + ' -- ' + ','.join([unicode(schedule) for schedule in task.schedules.all()]) + '\n'
    return HttpResponse(raw, content_type="text/plain")