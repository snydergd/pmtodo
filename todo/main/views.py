
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def taskView(request):
    context = {}
    if request.method == 'POST':
        context['task'] = request.form['task']
    return render(request, 'tasks/modify.html', context)

def userView(request):
    return HttpResponse("List of tasks")

def scheduleView(request):
    pass

def repeatView(request):
    pass
