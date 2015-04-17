from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/modify.html', views.taskView, name='task_view'),
    url(r'^tasks/due.html', views.dueTaskList, name='due_task_list'),
    url(r'^tasks/', views.taskList, name='task_list'),
    url(r'^repeats/modify.html', views.repeatView, name='repeat_view'),
    url(r'^repeats/', views.repeatList, name='repeat_list'),
    url(r'^schedules/modify.html', views.scheduleView, name='schedule_view'),
    url(r'^schedules/', views.scheduleList, name='schedule_list'),
    url(r'^', views.taskList, name='task_list'),
)
