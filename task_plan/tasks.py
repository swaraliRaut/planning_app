from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_POST

from task_plan.model_utils import get_users_vote_for_task
from task_plan.models import Task, Vote


@login_required
def show(request, task_code):
    try:
        task = Task.objects.get(id=int(task_code))
        user = get_user(request)
        choice = get_users_vote_for_task(task, user)
        return render(request, "task.html", {"task": task, "vote_list": Vote.possible_votes, "choice": choice, "error": None})
    except Task.DoesNotExist:
        return render(request, "task.html", {"task": None, "error": "Invalid task"})


@login_required
@require_POST
def create(request):
    task_name = request.POST.get('task_name')
    desc = request.POST.get('task_desc')
    user = get_user(request)
    new_task = Task.objects.create(name=task_name, desc=desc, owner=user)
    return redirect(reverse('show_task', args= (new_task.id, )))
