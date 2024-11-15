from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,)
    ph_no=models.IntegerField(unique=True)
    branch=models.CharField(max_length=25)
    batch_code = models.CharField(max_length=26, blank=False,default="A1")  # Required in forms


