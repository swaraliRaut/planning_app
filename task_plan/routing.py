from django.conf.urls import url
from task_plan.consumers import TaskConsumer

websocket_urlpatterns = [
    url(r'^ws/task/(?P<task_code>\w+)/$', TaskConsumer.as_asgi()),
]