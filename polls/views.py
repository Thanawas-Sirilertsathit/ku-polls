import logging
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from .utils import get_client_ip

logger = logging.getLogger("polls")


class IndexView(generic.ListView):
    """Index page"""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    """Display choices and question of a poll and allow voting"""
    model = Question
    template_name = "polls/question_detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        """Handle the dispatch with check if the poll can be voted or not"""
        try:
            question = self.get_object()
        except Http404:
            logger.error(
                f"Invalid poll access attempt. Redirecting to index page.")
            return redirect(reverse('polls:index'))

        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return HttpResponseRedirect(reverse('polls:index'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get user data"""
        context = super().get_context_data(**kwargs)
        user_vote = None
        if self.request.user.is_authenticated:
            try:
                user_vote = Vote.objects.get(
                    user=self.request.user, choice__question=self.get_object())
            except Vote.DoesNotExist:
                user_vote = None

        context['user_vote'] = user_vote
        return context


class ResultsView(generic.DetailView):
    """Render result page"""
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        """Get user data"""
        context = super().get_context_data(**kwargs)
        user_vote = None
        if self.request.user.is_authenticated:
            try:
                user_vote = Vote.objects.get(
                    user=self.request.user, choice__question=self.get_object())
            except Vote.DoesNotExist:
                user_vote = None

        context['user_vote'] = user_vote
        return context


@login_required
def vote(request, question_id):
    """Function for attempt voting that will create or change attribute choice if success then redirect"""
    question = get_object_or_404(Question, pk=question_id)
    ip = get_client_ip(request)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice.")
        logger.warning(
            f"User {request.user.username} failed to vote for question {question_id} from IP {ip}.")
        return render(
            request,
            "polls/question_detail.html",
            {"question": question, },
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
        logger.info(
            f'User {current_user.username} changed their vote to "{selected_choice.choice_text}" in "{question}" from IP {ip}.')
        logger.info(
            f'Question id : {question.id}, Choice : {selected_choice.id}')
        messages.success(
            request, f"Your vote was changed to '{selected_choice.choice_text}'.")
    except Vote.DoesNotExist:
        # If the user hasn't voted yet, create a new vote
        Vote.objects.create(user=current_user, choice=selected_choice)
        logger.info(
            f'User {current_user.username} voted for "{selected_choice.choice_text}" in "{question}" from IP {ip}.')
        logger.info(
            f'Question id : {question.id}, Choice : {selected_choice.id}')
        messages.success(
            request, f"You voted for '{selected_choice.choice_text}'.")

    # Redirect to the results page
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
