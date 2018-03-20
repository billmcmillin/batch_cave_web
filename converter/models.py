from django.db import models

# Create your models here.
class Conversion(models.Model):
    name = models.TextField(default='')
