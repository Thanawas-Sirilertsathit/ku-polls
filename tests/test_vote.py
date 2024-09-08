from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from polls.models import Poll, Choice, Vote
from datetime import timedelta


class VoteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.now = timezone.now()
        self.poll = Poll.objects.create(
            question="Test Poll?",
            pub_date=self.now - timedelta(days=1),
            end_date=self.now + timedelta(days=1)
        )
        self.choice1 = Choice.objects.create(
            poll=self.poll, choice_text="Choice 1")
        self.choice2 = Choice.objects.create(
            poll=self.poll, choice_text="Choice 2")

    def test_user_can_vote(self):
        """Test that a user can vote for a choice in a poll."""
        self.poll.vote(user=self.user, choice=self.choice1)
        vote = Vote.objects.get(user=self.user, poll=self.poll)
        self.assertEqual(vote.choice, self.choice1)

    def test_user_cannot_vote_twice(self):
        """Test that a user cannot vote more than once in the same poll."""
        self.poll.vote(user=self.user, choice=self.choice1)
        with self.assertRaises(Exception):
            self.poll.vote(user=self.user, choice=self.choice2)

    def test_cannot_vote_on_closed_poll(self):
        """Test that a user cannot vote on a poll that is closed."""
        closed_poll = Poll.objects.create(
            question="Closed Poll?",
            pub_date=self.now - timedelta(days=2),
            end_date=self.now - timedelta(days=1)
        )
        choice = Choice.objects.create(
            poll=closed_poll, choice_text="Closed Poll Choice")
        with self.assertRaises(Exception):
            closed_poll.vote(user=self.user, choice=choice)

    def test_cannot_vote_before_poll_published(self):
        """Test that a user cannot vote on a poll that is not yet published."""
        future_poll = Poll.objects.create(
            question="Future Poll?",
            pub_date=self.now + timedelta(days=1),
            end_date=self.now + timedelta(days=2)
        )
        choice = Choice.objects.create(
            poll=future_poll, choice_text="Future Poll Choice")
        with self.assertRaises(Exception):
            future_poll.vote(user=self.user, choice=choice)

    def test_vote_count_increments(self):
        """Test that the vote count increments correctly when a vote is cast."""
        initial_vote_count = self.choice1.votes
        self.poll.vote(user=self.user, choice=self.choice1)
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, initial_vote_count + 1)

    def test_multiple_users_can_vote(self):
        """Test that multiple users can vote in the same poll."""
        user2 = User.objects.create_user(
            username='testuser2', password='password')
        self.poll.vote(user=self.user, choice=self.choice1)
        self.poll.vote(user=user2, choice=self.choice2)

        vote1 = Vote.objects.get(user=self.user, poll=self.poll)
        vote2 = Vote.objects.get(user=user2, poll=self.poll)

        self.assertEqual(vote1.choice, self.choice1)
        self.assertEqual(vote2.choice, self.choice2)
