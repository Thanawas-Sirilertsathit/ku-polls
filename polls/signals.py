import logging
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .utils import get_client_ip

# Get the logger for this module
logger = logging.getLogger('polls')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    logger.info(f'User {user.username} logged in from IP {ip}.')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    logger.info(f'User {user.username} logged out from IP {ip}.')
