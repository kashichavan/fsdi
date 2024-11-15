from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from student.models import Student

class Company(models.Model):
    name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=30, unique=True)
    requirement_date = models.DateField(auto_now_add=True)
    is_scheduled = models.BooleanField(default=False)
    schedule_date = models.DateField(null=True, blank=True)
    students = models.ManyToManyField(Student, related_name="companies", blank=True)



    def __str__(self):
        return self.name

    def clean(self):
        if self.is_scheduled and not self.schedule_date:
            raise ValidationError("Schedule date must be set if the company is scheduled.")
        elif not self.is_scheduled:
            self.schedule_date = None  # Clear schedule date if not scheduled

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        