from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

USER_TYPE_CHOICES = [
    ('admin', 'admin'),
    ('customer', 'customer')
]

class BakeryUser(AbstractUser):
    
    user_type = models.CharField(max_length=40,choices=USER_TYPE_CHOICES)

# Create your models here.
