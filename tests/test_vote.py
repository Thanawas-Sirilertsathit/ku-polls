from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from polls.models import Question, Choice


class VoteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.poll = Question.objects.create(
            question_text='Test Poll', pub_date=timezone.now() - timezone.timedelta(days=1))
        self.choice1 = Choice.objects.create(
            question=self.poll, choice_text='Choice 1')
        self.choice2 = Choice.objects.create(
            question=self.poll, choice_text='Choice 2')

    def test_user_can_vote(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('polls:vote', args=[self.poll.id]), {
            'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.choice1.vote_set.count(), 1)

    def test_vote_count_increments(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('polls:vote', args=[self.poll.id]), {
            'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.choice1.vote_set.count(), 1)

    def test_multiple_users_can_vote(self):
        other_user = User.objects.create_user(
            username='otheruser', password='otherpassword')
        self.client.login(username='testuser', password='testpassword')
        self.client.post(reverse('polls:vote', args=[self.poll.id]), {
            'choice': self.choice1.id})
        self.client.logout()
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(reverse('polls:vote', args=[self.poll.id]), {
            'choice': self.choice2.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.choice1.vote_set.count(), 1)
        self.assertEqual(self.choice2.vote_set.count(), 1)
