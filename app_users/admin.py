from django.contrib import admin
from app_users.models import UserProfile, LoginHistory


class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'birthday', 'gender', 'update_date')
    date_hierarchy = 'birthday'
    list_display = ('user', 'birthday', 'gender', 'update_date')


class LoginHistoryAdmin(admin.ModelAdmin):
    list_filter = (
        'user', 'login_date', 'logout_date', 'cnt_activity', 'user_agent', 'ip_address', 'failed_login_attempts',
        'cnt_modification', 'cnt_entries', 'cnt_deleted', 'cnt_all_deleted')
    date_hierarchy = 'login_date'
    list_display = (
        'user', 'login_date', 'logout_date', 'cnt_activity', 'user_agent', 'ip_address', 'failed_login_attempts',
        'cnt_modification', 'cnt_entries', 'cnt_deleted', 'cnt_all_deleted')


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(LoginHistory, LoginHistoryAdmin)
