import logging
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from polls.models import Choice, Question, Vote


class LoggingTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.question = Question.objects.create(
            question_text='Sample Question', pub_date=timezone.now())
        self.choice = Choice.objects.create(
            question=self.question, choice_text='Choice 1')
        # Adjust the URL name to your login URL
        self.login_url = reverse('login')
        self.vote_url = reverse('polls:vote', args=[self.question.id])

    def test_failed_login_logging(self):
        """Test that a failed login attempt is logged correctly."""
        with self.assertLogs('polls', level='WARNING') as log:
            response = self.client.post(
                self.login_url, {'username': self.username, 'password': 'wrongpassword'})
        self.assertIn('Failed login attempt for user testuser', log.output[0])

    def test_invalid_poll_access_logging(self):
        """Test logging when accessing an invalid poll."""
        invalid_poll_id = 9999
        with self.assertLogs('polls', level='WARNING') as log:
            response = self.client.get(
                reverse('polls:detail', args=[invalid_poll_id]))
        self.assertRedirects(response, reverse('polls:index'))
        self.assertIn('Invalid poll access attempt', log.output[0])

    def test_vote_logging(self):
        """Test that voting is logged correctly."""
        self.client.login(username=self.username, password=self.password)
        with self.assertLogs('polls', level='INFO') as log:
            response = self.client.post(
                self.vote_url, {'choice': self.choice.id})
        self.assertIn(
            f'User {self.username} voted for "{self.choice.choice_text}"', log.output[0])

    def test_change_vote_logging(self):
        """Test that changing a vote is logged correctly."""
        self.client.login(username=self.username, password=self.password)
        Vote.objects.create(user=self.user, choice=self.choice)
        new_choice = Choice.objects.create(
            question=self.question, choice_text='Choice 2')
        with self.assertLogs('polls', level='INFO') as log:
            response = self.client.post(
                self.vote_url, {'choice': new_choice.id})
        self.assertIn(
            f'User {self.username} changed their vote to "{new_choice.choice_text}"', log.output[0])
