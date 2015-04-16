
from django import forms
from main.models import Task, Schedule, Repeat

        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['id', 'name', 'desc', 'date_created', 'schedules']
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id', 'repeat', 'start_date']
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class RepeatForm(forms.ModelForm):
    class Meta:
        model = Repeat
        fields = ['id', 'name', 'day', 'week', 'month', 'year']
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
