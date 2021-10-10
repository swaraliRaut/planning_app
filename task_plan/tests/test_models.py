from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from django.test import TestCase
from task_plan.models import Task, Vote
from task_plan.model_utils import get_users_vote_for_task
from django.contrib.auth import get_user_model



class TestTask(TestCase):
    def setUp(self):
        user_model = get_user_model()
        user1 = user_model.objects.create(username="user1", password="abc")
        Task.objects.create(name="task1", desc="sample desc", owner=user1)

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_object_labels(self):
        task = Task.objects.get(id=1)
        name_label = task._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'task name')
        desc_label = task._meta.get_field('desc').verbose_name
        self.assertEqual(desc_label, 'task description')

    def test_str(self):
        task = Task.objects.get(id=1)
        self.assertEqual(str(task), "task name: " + task.name + "desc: " + task.desc)

    def test_filed_length(self):
        task = Task.objects.get(id=1)
        name_max_length = task._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 100)
        desc_max_length = task._meta.get_field('desc').max_length
        self.assertEqual(desc_max_length, 600)

    def test_not_null_params(self):
        task = Task.objects.get(id=1)
        task.name = None
        self.assertRaises(IntegrityError, task.save)


class TestVote(TestCase):
    def setUp(self):
        user_model = get_user_model()
        user1 = user_model.objects.create(username="user1", password="abc")
        task1 = Task.objects.create(name="task1", desc="sample desc", owner=user1)
        Vote.objects.create(choice=1, voter=user1, task=task1)

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_object_labels(self):
        vote = Vote.objects.get(id=1)
        choice_label = vote._meta.get_field('choice').verbose_name
        self.assertEqual(choice_label, 'vote choice')

    def test_str(self):
        vote = Vote.objects.get(id=1)
        self.assertEqual(str(vote), "Voter: " + vote.voter.username + "choice: " + vote.choice)

    def test_filed_length(self):
        vote = Vote.objects.get(id=1)
        choice_max_length = vote._meta.get_field('choice').max_length
        self.assertEqual(choice_max_length, 3)

    def test_valid_value(self):
        vote = Vote.objects.get(id=1)
        vote.choice = 12
        self.assertRaises(ValidationError, vote.full_clean)


class ModelUtilsTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create(username="user1", password="abc")
        self.task = Task.objects.create(name="task1", desc="sample desc", owner=self.user)
        self.vote = Vote.objects.create(choice=1, voter=self.user, task=self.task)

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_get_users_vote_for_task(self):
        self.assertEqual(get_users_vote_for_task(self.task, self.user), self.vote.choice)
        self.assertEqual(1, 0)
