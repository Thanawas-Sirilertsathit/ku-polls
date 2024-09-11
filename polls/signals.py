"""Send signal and logging."""
import logging
from django.dispatch import receiver, Signal
from .utils import get_client_ip
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

# Custom signal for signup failure
signup_failed = Signal()

# Configure logger
logger = logging.getLogger('polls')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log message when user login."""
    ip = get_client_ip(request) if request else 'Unknown IP'
    logger.info(f'User {user.username} logged in from IP {ip}.')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log message when user logout."""
    ip = get_client_ip(request) if request else 'Unknown IP'
    logger.info(f'User {user.username} logged out from IP {ip}.')


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Log message when user login fail."""
    ip = get_client_ip(request) if request else 'Unknown IP'
    username = credentials.get('username', 'Unknown')
    logger.warning(f'Failed login attempt for user {username} from IP {ip}.')


@receiver(signup_failed)
def log_signup_failed(sender, request, **kwargs):
    """Log message when user signup fail."""
    ip = get_client_ip(request) if request else 'Unknown IP'
    username = kwargs.get('username', 'Unknown')
    logger.warning(f'Failed sign-up attempt for user {username} from IP {ip}.')
