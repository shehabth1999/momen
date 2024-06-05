from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
    amount = models.PositiveIntegerField(default=0)
    pass
