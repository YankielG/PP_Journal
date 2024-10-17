# Generated by Django 5.0.8 on 2024-10-17 17:36

import app_users.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_date', models.DateTimeField(auto_now_add=True, validators=[app_users.models.validate_date])),
                ('logout_date', models.DateTimeField(blank=True, null=True, validators=[app_users.models.validate_date])),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('failed_login_attempts', models.IntegerField(default=0)),
                ('cnt_modification', models.IntegerField(default=0)),
                ('cnt_entries', models.IntegerField(default=0)),
                ('cnt_deleted', models.IntegerField(default=0)),
                ('cnt_all_deleted', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, validators=[app_users.models.validate_date])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
