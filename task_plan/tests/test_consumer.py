import json
from unittest.mock import patch

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.testing import WebsocketCommunicator
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.test import TestCase

from task_plan.consumers import TaskConsumer
from task_plan.model_utils import get_vote_count_for_task_code, vote_for_task


class ConsumerTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user.save()
        login_success = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

    @patch("task_plan.consumers.vote_for_task", return_value="")
    @patch("task_plan.consumers.get_vote_count_for_task_code", return_value={"mock": "mock"})
    @patch("task_plan.consumers.redis_instance.get", return_value=json.dumps(
        {'0': 1, '0.5': 0, '1': 1, '2': 0, '3': 0, '5': 0, '8': 0, '13': 0}))
    async def test_get_from_redis(self, mocked_vote_for_task, mocked_get_vote_count_for_task_code, redis_mock):
        application = AuthMiddlewareStack(URLRouter([
            url(r'^ws/task/(?P<task_code>\w+)/$', TaskConsumer.as_asgi()),
        ]))
        communicator = WebsocketCommunicator(application, "/ws/task/1/")
        connected, subprotocol = await communicator.connect()
        self.assertEqual(connected, True)

        data = {"task_code": "1", "current_choice": "0", "new_choice": "1"}

        await communicator.send_to(json.dumps({"event": "UPDATE", "data": data}))
        response = await communicator.receive_from()
        count_dict = {'count': {'0': 0, '0.5': 0, '1': 2, '13': 0, '2': 0, '3': 0, '5': 0, '8': 0},
                      'event': 'update'}
        self.assertEqual(json.loads(response), count_dict)
        self.assertTrue(mocked_vote_for_task.called)
        self.assertTrue(redis_mock.called)
        self.assertFalse(mocked_get_vote_count_for_task_code.called)

        await communicator.disconnect()

    @patch("task_plan.consumers.vote_for_task", return_value="")
    @patch("task_plan.consumers.get_vote_count_for_task_code", return_value=
        {'0': 1, '0.5': 0, '1': 1, '2': 0, '3': 0, '5': 0, '8': 0, '13': 0})
    @patch("task_plan.consumers.redis_instance.get", return_value=None)
    async def test_get_from_redis(self, mocked_vote_for_task, mocked_get_vote_count_for_task_code, redis_mock):
        application = AuthMiddlewareStack(URLRouter([
            url(r'^ws/task/(?P<task_code>\w+)/$', TaskConsumer.as_asgi()),
        ]))
        communicator = WebsocketCommunicator(application, "/ws/task/1/")
        connected, subprotocol = await communicator.connect()
        self.assertEqual(connected, True)

        data = {"task_code": "1", "current_choice": "0", "new_choice": "1"}

        await communicator.send_to(json.dumps({"event": "UPDATE", "data": data}))
        response = await communicator.receive_from()
        count_dict = {'count': {'0': 1, '0.5': 0, '1': 1, '13': 0, '2': 0, '3': 0, '5': 0, '8': 0},
                      'event': 'update'}
        self.assertEqual(json.loads(response), count_dict)
        self.assertTrue(mocked_vote_for_task.called)
        self.assertTrue(redis_mock.called)
        self.assertTrue(mocked_get_vote_count_for_task_code.called)

        await communicator.disconnect()
