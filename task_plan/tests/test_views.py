from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_plan.models import Task, Vote


class ViewTest(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('')
        self.assertRedirects(response, '/log_in?next=/', fetch_redirect_response=False)

    def test_index_get_response(self):
        login_success = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertEqual(login_success, True)
        response = self.client.get('')
        self.assertEqual(str(response.context['user']), self.test_user.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
    def test_index_post_response(self):
        login_success = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertEqual(login_success, True)
        response = self.client.post('', data={'task_code': 1})
        self.assertRedirects(response, reverse('show_task', args=(1, )))


class TaskViewTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('show_task', args=(1, )))
        self.assertRedirects(response, '/log_in?next=/task/1', fetch_redirect_response=False)

    def test_task_response_for_invalid_task(self):
        login_success = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertEqual(login_success, True)
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task.html')
        self.assertEqual(response.context['task'], None)

    def test_task_response_for_valid_task(self):
        task = Task.objects.create(name="task1", desc="sample desc", owner=self.test_user)
        login_success = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertEqual(login_success, True)
        response = self.client.get('/task/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task.html')
        self.assertEqual(response.context['task'], task)
