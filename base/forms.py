from statistics import mode
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Task
from .widgets import DatePickerInput, TimePickerInput


class signUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)


class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('user', 'status')

        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput()
        }


class UserChangeProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        help_texts = {
            'password': 'Hello ',
        }
