from channels.db import database_sync_to_async
from django.db.models import Count

from task_plan.models import Task, Vote


def get_users_vote_for_task(task, user):
    choice = None
    vote = task.vote_set.filter(voter=user).first()
    if vote:
        choice = vote.choice
    return choice


@database_sync_to_async
def get_vote_count_for_task_code(task_code):
    vote_dict = {}
    for v in Vote.possible_votes:
        vote_dict[v] = 0
    vote_list = Vote.objects.filter(task_id=task_code).values_list('choice').annotate(choice_count=Count('choice'))

    for vote in vote_list:
        vote_dict[vote[0]] = vote[1]

    return vote_dict


@database_sync_to_async
def vote_for_task(task_code, choice, user):
    v = Vote.objects.update_or_create(voter=user, task_id=task_code, defaults={'choice': choice})
