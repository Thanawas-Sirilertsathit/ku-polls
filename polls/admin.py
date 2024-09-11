"""Module for admin related actions."""
from django.contrib import admin
from .models import Choice, Question
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mysite.forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    """Admin can create user."""

    add_form = CustomUserCreationForm
    form = CustomUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('password1', 'password2')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ChoiceInline(admin.StackedInline):
    """Admin can create choices for question."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Admin can create questions."""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": [
         "pub_date", "end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date",
                    "end_date", "was_published_recently"]


admin.site.register(Question, QuestionAdmin)
