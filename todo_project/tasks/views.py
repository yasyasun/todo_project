from rest_framework import permissions, generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Task, TaskPermission
from .serializers import TaskSerializer, TaskPermissionSerializer


class TaskView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        user = self.request.user
        return Task.objects.filter(id=task_id, creator=user) \
            or Task.objects.filter(id=task_id, permissions__user=user)

    def destroy(self, request, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        if task.creator != request.user:
            return Response({"detail": "У вас нет прав на выполнение данного действия."},
                            status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        task_id = self.kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Задача не найдена.")
        if task.creator == request.user or task.permissions.filter(user=request.user, permission='update').exists():
            serializer = self.get_serializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "У вас нет прав на выполнение данного действия."},
                            status=status.HTTP_403_FORBIDDEN)


class PermissionManageView(generics.GenericAPIView):
    serializer_class = TaskPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        if task.creator != request.user:
            return Response({"detail": "У вас нет прав на выполнение данного действия."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id)

        if task.creator != request.user:
            return Response({"detail": "У вас нет прав на выполнение данного действия."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            permission = TaskPermission.objects.get(task=task, user=request.user)
            permission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TaskPermission.DoesNotExist:
            return Response({"detail": "Прав доступа не найдено."}, status=status.HTTP_404_NOT_FOUND)
