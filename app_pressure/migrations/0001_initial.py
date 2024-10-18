# Generated by Django 5.0.8 on 2024-10-18 20:53

import app_pressure.models
import django.core.validators
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
            name='Pressure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shrink', models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(200)])),
                ('diastole', models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(150)])),
                ('pulse', models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(150)])),
                ('creation_date', models.DateTimeField(validators=[app_pressure.models.validate_date])),
                ('update_date', models.DateTimeField(auto_now=True, validators=[app_pressure.models.validate_date])),
                ('cnt_modification', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=255, validators=[django.core.validators.MaxLengthValidator(150)])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
