from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField("Bio", max_length=600, default='', blank=True)

    avatar = models.ImageField(null=True, default='user.svg')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username 