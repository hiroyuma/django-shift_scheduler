#shifts/models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} - {self.date}"