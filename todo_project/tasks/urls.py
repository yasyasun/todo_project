from django.urls import path
from .views import TaskView, TaskManageView, PermissionManageView

urlpatterns = [
    path('', TaskView.as_view(), name='tasks'),
    path('<int:pk>/', TaskManageView.as_view(), name='task_manage'),
    path('<int:task_id>/permissions/', PermissionManageView.as_view(), name='permission_manage'),
]
