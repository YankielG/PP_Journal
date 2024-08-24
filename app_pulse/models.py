from django.db import models

# Create your models here.
class Pulse(models.Model):
    pulse = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateTimeField()
    comments = models.CharField(max_length=255)

    def __str__(self):
        return f'Tetno: {self.pulse} Data: {self.date} Uwagi: {self.comments}'

