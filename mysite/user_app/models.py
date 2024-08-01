from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    # bio = models.TextField(blank=True)
    # avatar = models.ImageField(upload_to='avatars', blank=True)

    def __str__(self):
        return self.username
