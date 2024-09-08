from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from datetime import timedelta


class PollModelTest(TestCase):

    def setUp(self):
        self.now = timezone.now()

    def test_is_published_future_poll(self):
        """Test that a poll is not published if its pub_date is in the future."""
        future_poll = Question.objects.create(
            question_text="Future Poll?",
            pub_date=self.now + timedelta(days=1),
            end_date=self.now + timedelta(days=2)
        )
        self.assertFalse(future_poll.is_published())

    def test_is_published_current_poll(self):
        """Test that a poll is published if its pub_date is now."""
        current_poll = Question.objects.create(
            question_text="Current Poll?",
            pub_date=self.now,
            end_date=self.now + timedelta(days=1)
        )
        self.assertTrue(current_poll.is_published())

    def test_is_published_past_poll(self):
        """Test that a poll is published if its pub_date is in the past."""
        past_poll = Question.objects.create(
            question_text="Past Poll?",
            pub_date=self.now - timedelta(days=1),
            end_date=self.now + timedelta(days=1)
        )
        self.assertTrue(past_poll.is_published())

    def test_can_vote_before_start(self):
        """Test that can_vote is False before the poll starts."""
        not_started_poll = Question.objects.create(
            question_text="Not Started Poll?",
            pub_date=self.now + timedelta(days=1),
            end_date=self.now + timedelta(days=2)
        )
        self.assertFalse(not_started_poll.can_vote())

    def test_can_vote_after_end(self):
        """Test that can_vote is False after the poll ends."""
        ended_poll = Question.objects.create(
            question_text="Ended Poll?",
            pub_date=self.now - timedelta(days=2),
            end_date=self.now - timedelta(days=1)
        )
        self.assertFalse(ended_poll.can_vote())

    def test_can_vote_during_voting_period(self):
        """Test that can_vote is True during the voting period."""
        open_poll = Question.objects.create(
            question_text="Open Poll?",
            pub_date=self.now - timedelta(days=1),
            end_date=self.now + timedelta(days=1)
        )
        self.assertTrue(open_poll.can_vote())

    def test_can_vote_exact_start(self):
        """Test that can_vote is True exactly at the poll start time."""
        exact_start_poll = Question.objects.create(
            question_text="Exact Start Poll?",
            pub_date=self.now,
            end_date=self.now + timedelta(days=1)
        )
        self.assertTrue(exact_start_poll.can_vote())
