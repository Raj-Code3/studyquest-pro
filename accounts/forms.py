from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    class Meta:
        model  = User
        fields = ['username','first_name','last_name','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username':'Choose a username','first_name':'First name',
            'last_name':'Last name','email':'your@email.com',
            'password1':'Create password','password2':'Confirm password'
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control','placeholder':placeholders.get(name,'')})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username or email'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Password'})

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    email      = forms.EmailField()
    class Meta:
        model  = Profile
        fields = ['phone','bio','profile_picture']
        widgets = {'bio': forms.Textarea(attrs={'rows':3})}
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial  = user.last_name
            self.fields['email'].initial      = user.email
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
