from django.db import models
from django.conf import settings


class Task(models.Model):
    name = models.CharField(max_length=300)
    desc = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return ""


class Vote(models.Model):
    possible_votes = ["0", "0.5", "1", "2", "3", "5", "8", "13"]
    VOTE_CHOICES = [ (v, v) for v in possible_votes ]
    choice = models.CharField(max_length=3, choices=VOTE_CHOICES, default=None)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE, default=None)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("voter", "task")
