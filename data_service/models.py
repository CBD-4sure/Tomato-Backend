from turtle import title
from django.db import models

# Create your models here.

class RestdataTable(models.Model):
    data = models.JSONField()
    res_id = models.IntegerField()

class MenuDataTable(models.Model):
    resId = models.IntegerField()
    title = models.CharField(max_length=100)
    data = models.JSONField()