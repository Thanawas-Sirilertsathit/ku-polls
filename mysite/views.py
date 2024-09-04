from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib import messages


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been created! You are now logged in.')
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
