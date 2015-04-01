from django.conf.urls import patterns, include, url

from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^task/', views.task_view, name='task_view'),
)
