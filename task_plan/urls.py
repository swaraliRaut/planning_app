from django.urls import path

from task_plan.tasks import create, show

urlpatterns = [
    path('create', create, name="create"),
    path('<task_code>', show, name="show_task")
]
