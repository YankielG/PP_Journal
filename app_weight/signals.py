from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.contrib.auth.models import User
from user_agents import parse
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Weight
from app_users.models import UserProfile, LoginHistory

