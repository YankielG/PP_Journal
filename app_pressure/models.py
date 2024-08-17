from django.db import models

# Create your models here.
class Pressure(models.Model):
    shrink = models.DecimalField(max_digits=3, decimal_places=1 ) # skurczowe
    diastole = models.DecimalField(max_digits=3, decimal_places=1 ) # rozkurczowe
    pulse = models.DecimalField(max_digits=3, decimal_places=1)
    date = models.DateTimeField()
    comments = models.CharField(max_length=255)

    # def __str__(self):
    #     return f'Cis_skurcz: {self.shrink} Cis_rozkurcz: {self.diastole} Puls: {self.pulse} Data: {self.date} Uwagi: {self.comments}'