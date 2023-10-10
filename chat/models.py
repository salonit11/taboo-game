from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Room(models.Model):
    """Model definition for Room."""
    name = models.CharField('Name', max_length=250)
    users=models.ManyToManyField(User)
    code= models.CharField(max_length=6,unique=True)
    # TODO: Define fields here

    
    def __str__(self):
        """Unicode representation of Room."""
        return self.code

class Word(models.Model):
    words=models.TextField()
    difficulty=models.CharField(max_length=20)
    score=models.IntegerField()