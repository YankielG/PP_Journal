from datetime import datetime, timedelta
import time
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile, LoginHistory


class EndActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = request.user
            login_history = LoginHistory.objects.filter(user=user).last()
            login_history.logout_date = datetime.now()
            login_date = login_history.login_date.replace(tzinfo=None)
            login_history.cnt_activity = round((datetime.now() - login_date).total_seconds()/60)
            login_history.save()
        return response