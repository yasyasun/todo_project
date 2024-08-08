from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TaskPermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('update', 'Update'),
    ]

    user = models.ForeignKey(User, related_name='permissions', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='permissions', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('user', 'task', 'permission')
