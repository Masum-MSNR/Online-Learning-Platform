import email
from enum import unique
from bson import is_valid
from django import forms
from django.contrib.auth import authenticate
from base.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=30)
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    genders = [('Male', 'Male'), ('Female', 'Female')]
    gender = forms.ChoiceField(choices=genders, widget=forms.RadioSelect)
    date_of_birth = forms.DateField(widget=DateInput)
    types = [('Student', 'Student'), ('Publisher', 'Publisher')]
    account_type = forms.ChoiceField(choices=types, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'date_of_birth', 'gender', 'account_type']
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LogInForm(forms.ModelForm):
    mail = forms.EmailField(label='Email',max_length=30,widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['mail','password']
