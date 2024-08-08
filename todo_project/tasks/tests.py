from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from tasks.models import TaskPermission, Task


class TaskAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.task = Task.objects.create(title='Test Task', creator=self.user1)
        self.client.login(username='testuser1', password='testpass')

    def test_create_task(self):
        response = self.client.post(reverse('tasks'), {
            'title': 'New Task',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        self.client.post(reverse('tasks'), {
            'title': 'Test Task',
        })
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_read_task(self):
        response = self.client.get(reverse('task_manage', kwargs={'pk': self.task.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        data = {'title': 'Updated Title'}
        response = self.client.put(reverse('task_manage', kwargs={'pk': self.task.id}), data)
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.title, 'Updated Title')

    def test_delete_task(self):
        response = self.client.delete(reverse('task_manage', kwargs={'pk': self.task.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

