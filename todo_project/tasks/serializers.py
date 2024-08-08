from rest_framework import serializers
from .models import Task, TaskPermission


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title']


class TaskPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskPermission
        fields = ['user', 'permission']
