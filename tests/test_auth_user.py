"""Tests of authentication."""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # to "login" a user using code
from polls.models import Question, Choice
from mysite import settings


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        # superclass setUp creates a Client object and initializes test database
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester"
        self.user1.save()
        # we need a poll question to test voting
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_login_view(self):
        """A user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using a POST request
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser",
                     "password": "FatChance!"
                     }
        response = self.client.post(login_url, form_data)
        # after successful login, should redirect browser somewhere
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        response = self.client.get(reverse('polls:vote', args=[1]))
        # Adjust to the correct URL for login
        login_with_next = '/accounts/login/?next=/polls/1/vote/'
        self.assertRedirects(response, login_with_next)

    def test_login_error_message(self):
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        # Update the error message to match what Django returns
        self.assertContains(
            response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_login_failure(self):
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        # Update the error message to match what Django returns
        self.assertContains(
            response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_signup_error_message(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'differentpassword'
        })
        # Update the error message to match what Django returns
        self.assertContains(response, "The two password fields didn’t match.")

    def test_signup_failure(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'differentpassword'
        })
        # Update the error message to match what Django returns
        self.assertContains(response, "The two password fields didn’t match.")
