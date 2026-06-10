from django import forms
from .models import Task
from subjects.models import Subject

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title','description','subject','due_date','priority','status','xp_reward']
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
            'due_date':    forms.DateInput(attrs={'type':'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        self.fields['subject'].required = False
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
