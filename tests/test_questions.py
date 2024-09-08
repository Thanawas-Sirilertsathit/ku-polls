from datetime import timedelta
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.messages import get_messages
from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 redirection.
        """
        future_question = create_question(
            question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_voting_not_allowed(self):
        """
        If voting is not allowed, redirect to the polls index and show an error message.
        """
        question = Question.objects.create(
            question_text="Past Question.",
            pub_date=timezone.now() - timedelta(days=5),
            end_date=timezone.now() - timedelta(days=1)  # Voting period has ended
        )
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)

        # Check if redirected to the index page
        self.assertRedirects(response, reverse("polls:index"))

        # Check if the error message is set
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Voting is not allowed for this poll." in str(m) for m in messages))


class QuestionModelTests(TestCase):

    def test_is_published_with_future_pub_date(self):
        """
        is_published() returns False for questions whose pub_date is in the future.
        """
        future_question = Question(
            pub_date=timezone.now() + timedelta(days=30))
        self.assertFalse(future_question.is_published())

    def test_is_published_with_past_pub_date(self):
        """
        is_published() returns True for questions whose pub_date is in the past.
        """
        past_question = Question(pub_date=timezone.now() - timedelta(days=30))
        self.assertTrue(past_question.is_published())

    def test_is_published_with_default_pub_date(self):
        """
        is_published() returns True for questions with a pub_date of now.
        """
        now_question = Question(pub_date=timezone.now())
        self.assertTrue(now_question.is_published())

    def test_can_vote_before_pub_date(self):
        """
        can_vote() returns False for questions whose pub_date is in the future.
        """
        future_question = Question(pub_date=timezone.now() + timedelta(days=1))
        self.assertFalse(future_question.can_vote())

    def test_can_vote_after_end_date(self):
        """
        can_vote() returns False if the end_date is in the past.
        """
        past_question = Question(pub_date=timezone.now() - timedelta(days=10),
                                 end_date=timezone.now() - timedelta(days=1))
        self.assertFalse(past_question.can_vote())

    def test_can_vote_within_voting_period(self):
        """
        can_vote() returns True if current date is between pub_date and end_date.
        """
        question = Question(pub_date=timezone.now() - timedelta(days=1),
                            end_date=timezone.now() + timedelta(days=1))
        self.assertTrue(question.can_vote())
