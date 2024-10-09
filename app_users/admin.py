from django.contrib import admin
from app_users.models import UserProfile, LoginHistory

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'birthday', 'gender', 'update_date')
    date_hierarchy = 'birthday'
    list_display = ('user', 'birthday', 'gender', 'update_date')

class LoginHistoryAdmin(admin.ModelAdmin):
    list_filter = ('user', 'login_date')
    date_hierarchy = 'login_date'
    list_display = ('user', 'login_date')


# Register your models here.
# admin.site.register(UserProfile, LoginHistory)
# admin.site.register(UserProfileAdmin, LoginHistoryAdmin)