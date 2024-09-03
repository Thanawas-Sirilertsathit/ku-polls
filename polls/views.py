from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """Display choices and question of a poll and allow voting"""
    model = Question
    template_name = "polls/question_detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return HttpResponseRedirect(reverse('polls:index'))
        return super().dispatch(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/question_detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    # Reference to the current user
    current_user = request.user
    # Check if the user has already voted for this question
    try:
        user_vote = Vote.objects.get(
            user=current_user, choice__question=question)
        # Update the user's vote to the new choice
        user_vote.choice = selected_choice
        user_vote.save()
        messages.success(
            request, f"Your vote was changed to '{selected_choice.choice_text}'.")
    except Vote.DoesNotExist:
        # If the user hasn't voted yet, create a new vote
        Vote.objects.create(user=current_user, choice=selected_choice)
        messages.success(
            request, f"You voted for '{selected_choice.choice_text}'.")

    # Redirect to the results page
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
