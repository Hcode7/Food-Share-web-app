from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.models import User

class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('img' , 'bio')
        

class UsercreationForm(DefaultUserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self, *args,**kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if  password != password2:
            raise forms.ValidationError('Password Dont Match')
        return password2