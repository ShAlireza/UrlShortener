from django.contrib.auth.models import AbstractUser

from django.db import models


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    """
    Custom user for avoid the problems that may occur in future while we like
    to add some new features to our User model.
    """
    pass
