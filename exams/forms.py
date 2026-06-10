from django import forms
from .models import Exam
from subjects.models import Subject

class ExamForm(forms.ModelForm):
    class Meta:
        model  = Exam
        fields = ['exam_name','subject','exam_date','exam_type','location','notes']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type':'date'}),
            'notes':     forms.Textarea(attrs={'rows':3}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
