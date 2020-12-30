from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Game(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    words = models.CharField(max_length=500)

class Player(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher')
