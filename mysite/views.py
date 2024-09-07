import logging
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from polls.utils import get_client_ip
from polls.signals import signup_failed


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Message the system for success login"""
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)


logger = logging.getLogger('polls')


def signup(request):
    """Render signup page"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
        else:
            signup_failed.send(
                sender='register_view', request=request, username=request.POST.get('username'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
