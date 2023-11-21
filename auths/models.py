from django.contrib.auth.models import AbstractUser
from django.db import models
from teams.models import Team


class User(AbstractUser):
    username = models.CharField(
        max_length=128,
        unique=True,
    )  # 계정명
    is_manager = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='owner')