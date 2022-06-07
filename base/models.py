from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    profile_pic = models.ImageField(
        default="default_profile_pic.jpg")
    phone_no = models.BigIntegerField(validators=[
        MaxValueValidator(9999999999),
        MinValueValidator(1111111111)
    ], blank=False)


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        Pending = 'Pending'
        Done = 'Done'
        Due = 'Due'

    class Priority(models.TextChoices):
        High = 'High'
        Medium = 'Medium'
        Low = 'Low'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=128, blank=False)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.Pending)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.Low)

    def __str__(self):
        return self.task_name
