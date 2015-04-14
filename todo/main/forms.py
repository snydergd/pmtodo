
from django import forms
from main.models import Task, Schedule, Repeat

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'desc', 'date_created', 'schedules']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['repeat', 'start_date']

class RepeatForm(forms.ModelForm):
    class Meta:
        model = Repeat
        fields = ['id', 'name', 'day', 'week', 'month', 'year']
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
