from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=255, blank=True)
    img = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio = models.TextField()

