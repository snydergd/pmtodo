
from django import forms
from main.models import Task, Schedule, Repeat, Status
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['id', 'name', 'desc', 'date_created', 'schedules']
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    repeat = forms.ModelChoiceField(label="New Repeat by Type", queryset=Repeat.objects.all(), required=False)
    start_date = forms.DateField(label="New Repeat start date", required=False)

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

class StatusFormBasic(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['text', 'complete', 'date', 'task']
        widgets = {
            'task': forms.HiddenInput()
        }
    def handleInput(self):
        if self.is_valid():
            instance = self.save()
            return "OK" + str(instance.id)
        else:
            return "IVForm" + ", ".join([str(f.errors)+','+f.name for f in self])