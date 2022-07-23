from asyncio.format_helpers import extract_stack
import email
from enum import unique
from turtle import onclick
from bson import is_valid
from django import forms
from django.contrib.auth import authenticate
from base.models import Course, User, Video


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
    mail = forms.EmailField(label='Email', max_length=30,
                            widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['mail', 'password']


class CourseForm(forms.ModelForm):
    title = forms.CharField(max_length=500)
    types = [('Free', 'Free'), ('Paid', 'Paid')]
    course_type = forms.ChoiceField(choices=types, widget=forms.RadioSelect(attrs={
        'onclick': "btnSearch_Click()",
    }))

    class Meta:
        model = Course
        fields = ['coverImage', 'title', 'outcome',
                  'requirement', 'description', 'course_type', 'fee']
        widgets = {
            'outcome': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'requirement': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        }


class VideoForm(forms.ModelForm):

    video_file=forms.FileField(widget=forms.FileInput(attrs={'accept':'video/*'}))

    class Meta:
        model = Video
        fields=['title','video_file']
        


class TempForm(forms.Form):
    test = forms.CharField(max_length=20)
