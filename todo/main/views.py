
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Task

# Create your views here.

def taskView(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        task = None
        if 'id' in data and data['id'] != '':
            if not data['id'].isdigit():
                return HttpResponse("Invalid task id, must be a number")
            task = Task.objects.get(pk=int(data['id']))
        else:
            task = Task()
        for key, value in request.POST.iteritems():
            if hasattr(task, key) and value != '': setattr(task, key, value)
        task.save()
        if 'closeafter' in data:
            return redirect('tasks/list.html')
        context['task'] = task
    if request.GET and 'id' in request.GET and request.GET['id'].isdigit():
        context['task'] = Task.objects.get(pk=int(request.GET['id']))
    return render(request, 'tasks/modify.html', context)

def taskList(request):
    context = {}
    if request.method == "GET":
        data = request.GET
        if 'action' in data:
            if data['action'] == 'delete' and 'id' in data and data['id'].isdigit():
                Task.objects.get(pk=data['id']).delete()
    context['task_list'] = Task.objects.all()
    return render(request, 'tasks/list.html', context)
    
def userView(request):
    return HttpResponse("List of tasks")

def scheduleView(request):
    pass

def repeatView(request):
    pass
