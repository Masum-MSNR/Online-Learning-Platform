from statistics import mode
from django.db import models

class User(models.Model):
    mail=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    gender=models.CharField(max_length=20)
    date_of_birth=models.CharField(max_length=20)
    account_type=models.CharField(max_length=20)
