from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote


class CancelVoteTest(TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.question = Question.objects.create(
            question_text='Test Poll',
            pub_date=timezone.now() - timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=1)
        )
        self.choice1 = Choice.objects.create(
            question=self.question, choice_text='Choice 1')
        self.choice2 = Choice.objects.create(
            question=self.question, choice_text='Choice 2')
        self.client.login(username='testuser', password='testpassword')

    def test_cancel_vote(self):
        """Test that a user can cancel their vote."""
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), {
                                    'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vote.objects.filter(
            user=self.user, choice=self.choice1).exists())
        response = self.client.post(
            reverse('polls:cancel_vote', args=[self.question.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vote.objects.filter(
            user=self.user, choice=self.choice1).exists())

    def test_cancel_vote_without_casting(self):
        """Test that canceling a vote without casting a vote does not cause an error."""
        response = self.client.post(
            reverse('polls:cancel_vote', args=[self.question.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vote.objects.filter(user=self.user).count(), 0)
