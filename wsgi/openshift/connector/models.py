from django.db import models

# Create your models here.
class Member(models.Model):
	dummy = models.CharField(max_length=200)