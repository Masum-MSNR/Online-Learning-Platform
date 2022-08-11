from asyncio.windows_events import NULL
from cProfile import label
import imp
import random
import string
import os
from itertools import tee
from pyexpat import model
from statistics import mode
from time import time
from turtle import title
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import hashers
from django import forms
from pkg_resources import require
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    gender = models.CharField(max_length=30, default='Other')
    date_of_birth = models.CharField(max_length=60, default='00-00-00')
    account_type = models.CharField(max_length=30, default="Student")
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=300)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Comment:
    username = models.CharField(max_length=30)
    text = models.CharField()


class Course(models.Model):
    username = models.CharField(max_length=30)
    cover_image = models.ImageField(blank=True, null=True, upload_to="images/")
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    outcome = models.TextField()
    requirement = models.TextField()
    description = models.TextField()
    course_type = models.CharField(max_length=30, default='Free')
    fee = models.IntegerField(blank=True, null=True, default=0)
    time = models.DateTimeField(default=timezone.now)
    video_count = models.IntegerField(blank=True, null=True, default=0)
    rating=models.FloatField(default=0)
    number_of_rating=models.IntegerField(default=0)
    number_of_sold=models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        modified_name = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=20))
        ext = os.path.splitext(self.cover_image.name)[-1]
        new_name = modified_name+ext
        self.cover_image.name = new_name
        super(Course, self).save(*args, **kwargs)


class Video(models.Model):
    s_id = models.IntegerField(default=0)
    course_id = models.IntegerField(default=0)
    video_file = models.FileField(upload_to="videos/")
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        modified_name = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=20))
        ext = os.path.splitext(self.video_file.name)[-1]
        new_name = modified_name+ext
        self.video_file.name = new_name
        super(Video, self).save(*args, **kwargs)
        

class Cart(models.Model):
    course_id=models.IntegerField(default=0)
    username = models.CharField(max_length=30)
    

class StudentCourse(models.Model):
    course_id=models.IntegerField(default=0)
    username = models.CharField(max_length=30)
    


class Rating(models.Model):
    username=models.CharField(max_length=30,default=NULL)
    course_id=models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    description = models.CharField(null=True, blank=True, max_length=555)
