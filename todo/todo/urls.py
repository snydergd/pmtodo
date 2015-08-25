from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/(?P<task_id>\d+)/(?:(?P<action>\w+))?', views.taskView, name='task_view'),
    url(r'^tasks/(?P<action>add)', views.taskView, name='task_add'),
    url(r'^tasks/(?P<type>[^0-9]\w*)?', views.taskList, name='task_list'),
#    url(r'^tasks/', views.taskList, name='task_list'),
    url(r'^repeats/(?P<repeat_id>\d+)/(?:(?P<action>\w+))?', views.repeatView, name='repeat_view'),
    url(r'^repeats/(?P<action>add)', views.repeatView, name='repeat_add'),
    url(r'^repeats/', views.repeatList, name='repeat_list'),
    url(r'^schedules/modify.html', views.scheduleView, name='schedule_view'),
    url(r'^schedules/', views.scheduleList, name='schedule_list'),
    url(r'^statuses/', views.statusList, name='status_list'),
    url(r'^raw/', views.raw, name='raw'),
    url(r'^', views.taskList, name='task_list'),
)
