import imp
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import hashers
from django import forms


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


class Video:
    videoLink = models.CharField()
    thumbLink = models.CharField()
    type = models.CharField(max_length=30)


class Course:
    title = models.CharField()
    outcome = models.CharField()
    requirement = models.CharField()
    description = models.CharField()
    ratings = []
