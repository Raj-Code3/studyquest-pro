from django import forms
from .models import Subject

ICON_CHOICES = [
    ('📚','📚 Books'),('🔬','🔬 Science'),('🧮','🧮 Math'),('💻','💻 Computer'),
    ('🌍','🌍 Geography'),('📖','📖 Literature'),('🎨','🎨 Arts'),('⚗️','⚗️ Chemistry'),
    ('🧬','🧬 Biology'),('📐','📐 Engineering'),('🎵','🎵 Music'),('🏃','🏃 Sports'),
    ('💡','💡 Physics'),('📊','📊 Statistics'),('🗣️','🗣️ Language'),('🏛️','🏛️ History'),
]
COLOR_CHOICES = [
    ('#6366f1','Indigo'),('#ec4899','Pink'),('#14b8a6','Teal'),('#f59e0b','Amber'),
    ('#10b981','Emerald'),('#3b82f6','Blue'),('#ef4444','Red'),('#8b5cf6','Purple'),
]

class SubjectForm(forms.ModelForm):
    icon  = forms.ChoiceField(choices=ICON_CHOICES)
    color = forms.ChoiceField(choices=COLOR_CHOICES)
    class Meta:
        model  = Subject
        fields = ['subject_name','teacher_name','credits','description','icon','color']
        widgets = {'description': forms.Textarea(attrs={'rows':3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
