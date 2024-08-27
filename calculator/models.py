from django.db import models

# Create your models here.
from django.db import models

class Number(models.Model):
    value = models.IntegerField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
