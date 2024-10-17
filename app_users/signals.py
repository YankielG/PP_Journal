from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.auth.models import User
from user_agents import parse

from .models import UserProfile, LoginHistory

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    browser_info = f"{user_agent.browser.family} - {user_agent.browser.version_string}"

    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        ip = forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    session_id = request.session.session_key

    LoginHistory.objects.create(user=user, user_agent=browser_info, ip_address=ip, session_id=session_id)

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    if 'username' in credentials:
        username = credentials['username']
        try:
            user = User.objects.get(username=username)
            login_history = LoginHistory.objects.filter(user=user).last()
            if login_history:
                login_history.failed_login_attempts += 1
                login_history.save()
            else:
                user_agent_string = request.META.get('HTTP_USER_AGENT', '')
                user_agent = parse(user_agent_string)
                browser_info = f"{user_agent.browser.family} - {user_agent.browser.version_string}"

                forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
                if forwarded:
                    ip = forwarded.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                session_id = request.session.session_key

                LoginHistory.objects.create(
                    user=user, user_agent=browser_info, ip_address=ip, session_id=session_id, failed_login_attempts=1)

        except User.DoesNotExist:
            # Użytkownik nie istnieje
            pass
