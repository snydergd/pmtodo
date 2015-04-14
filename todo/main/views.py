
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Task, Repeat, Schedule
from main.forms import RepeatForm

# Create your views here.

def genericModView(request, t, context, typeName, foreign={}):
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
    context['all_schedules'] = Schedule.objects.all()
    return genericModView(request, Task, context, 'task')

def taskList(request):
    return genericListView(request, Task, {}, 'task')
    
def repeatView(request):
    instance = None
    if request.GET and 'id' in request.GET and request.GET['id'].isdigit():
        instance = Repeat.objects.get(pk=request.GET['id'])
    elif request.POST and 'id' in request.POST and request.POST['id'].isdigit():
        instance = Repeat.objects.get(pk=request.POST['id'])
    if request.method == "POST":
        form = RepeatForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    else:
        form = RepeatForm(instance=instance)
    return render(request, 'repeats/modify.html', {'form': form.as_p(), 'repeat': instance})

def repeatList(request):
    return genericListView(request, Repeat, {}, 'repeat')
    
def scheduleView(request):
    context = {}
    context['all_repeats'] = Repeat.objects.all()
    return genericModView(request, Schedule, context, 'schedule', foreign={'repeat': Repeat})

def scheduleList(request):
    return genericListView(request, Schedule, {}, 'schedule')
    
def userView(request):
    return HttpResponse("List of tasks")
