from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user
from task_plan.models import Task, Vote
from task_plan.model_utils import get_users_vote_for_task


@login_required
def show(request, task_code):
    try:
        #task_code = request.GET.get('task_code')
        print("show................................")
        #print(request.REQUEST.get("task_code"))
        task = Task.objects.get(id=int(task_code))
        user = get_user(request)
        choice = get_users_vote_for_task(task, user)
        print("choice", choice)
        return render(request, "task.html", {"task": task, "vote_list": Vote.possible_votes, "choice" : choice})
    except Task.DoesNotExist:
        return render(request, "task.html", {"task": None})

@login_required
@require_POST
def create(request):
    print(".......................................create")
    task_name = request.POST.get('task_name')
    desc = request.POST.get('task_desc')
    user = get_user(request)
    new_task = Task.objects.create(name=task_name, desc=desc, owner=user)
    print(new_task.id)
    return redirect(reverse('show_task', args= (new_task.id, )))
