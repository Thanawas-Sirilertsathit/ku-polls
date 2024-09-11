"""Create model of polls website."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """A question model in a poll."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return question text."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """Return True if published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if the current date-time is on or after the publication date."""
        return timezone.localtime() >= self.pub_date

    def can_vote(self):
        """Return True if the current date-time is between pub_date and end_date."""
        now = timezone.localtime()
        return self.pub_date <= now and (self.end_date is None or now <= self.end_date)


class Choice(models.Model):
    """A choice from a specific question in the poll."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Return choice text."""
        return self.choice_text

    @property
    def votes(self):
        """Return the votes of the choice."""
        return self.vote_set.count()


class Vote(models.Model):
    """A Vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for vote."""

        unique_together = ('user', 'choice')
