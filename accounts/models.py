from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    coach = models.BooleanField(null=True, blank=True, default=False)
