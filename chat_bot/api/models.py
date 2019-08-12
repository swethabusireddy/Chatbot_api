from django.db import models

# Create your models here.
class test(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.IntegerField(default = 0)