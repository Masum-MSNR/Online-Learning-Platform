from asyncio.format_helpers import extract_stack
import email
from enum import unique
from tkinter import Widget
from turtle import onclick
from bson import is_valid
from django import forms
from django.contrib.auth import authenticate
from base.models import Course, Rating, User, Video, Rating


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
    categories = [
        ('Academics', 'Academics'),
        ('Business', 'Business'),
        ('Design', 'Design'),
        ('Development', 'Development'),
        ('Health & Fitness', 'Health & Fitness'),
        ('IT & Software', 'IT & Software'),
        ('Language', 'Language'),
        ('Lifestyle', 'Lifestyle'),
        ('Marketing', 'Marketing'),
        ('Music', 'Music'),
        ('Office Productivity', 'Office Productivity'),
        ('Personal Development', 'Personal Development'),
        ('Photography', 'Photography')
    ]
    category = forms.ChoiceField(choices=categories)
    course_type = forms.ChoiceField(choices=types, widget=forms.RadioSelect(attrs={
        'onclick': "btnSearch_Click()",
    }))

    class Meta:
        model = Course
        fields = ['username', 'category', 'cover_image', 'title', 'outcome',
                  'requirement', 'description', 'course_type', 'fee']
        widgets = {
            'outcome': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'requirement': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'username': forms.HiddenInput(),
        }


class VideoForm(forms.ModelForm):
    video_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'video/*'})
    )

    class Meta:
        model = Video
        fields = ['course_id','s_id','duration', 'title', 'video_file']
        widgets = {
            'course_id': forms.HiddenInput(),
            's_id': forms.HiddenInput(),
            'duration': forms.HiddenInput(),
        }


class TempForm(forms.Form):
    test = forms.CharField(max_length=20)


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['username','course_id','rating', 'description']
        widgets = {
            'course_id': forms.HiddenInput(),
            'username': forms.HiddenInput(),
        }
