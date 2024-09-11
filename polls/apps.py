"""App config and signal set up."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Set up signals for logging."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        """Receive signals from server and log."""
        import polls.signals
