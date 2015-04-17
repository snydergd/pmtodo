from django.contrib import admin
from main.models import Task, Schedule, Repeat, Status

class StatusInline(admin.TabularInline):
    model = Status
    pass

class TaskAdmin(admin.ModelAdmin):
    inlines = [StatusInline]
    pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Repeat)
admin.site.register(Schedule)
