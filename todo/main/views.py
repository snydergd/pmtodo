
from django.shortcuts import render
from django.http import HttpResponse
from main.models import Task

# Create your views here.

def taskView(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        task = None
        if 'task' in data:
            if type(data['task']) != int:
                return HttpResponse("Invalid task id, must be an int")
            task = Task.objects.get(pk=data['task'])
        else:
            task = Task()
        for key, value in request.POST.iteritems():
            if hasattr(task, key): setattr(task, key, value)
        task.save()
        context['task'] = task
    return render(request, 'tasks/modify.html', context)

def userView(request):
    return HttpResponse("List of tasks")

def scheduleView(request):
    pass

def repeatView(request):
    pass
