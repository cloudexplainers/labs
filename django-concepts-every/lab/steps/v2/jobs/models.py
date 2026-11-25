from django.contrib.auth.models import User
from django.db import models


class Job(models.Model):
    address = models.CharField(max_length=100)
    client = models.CharField(max_length=60)

    def __str__(self):
        return self.address


class Task(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="tasks")
    room = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.room}: {self.title}"
