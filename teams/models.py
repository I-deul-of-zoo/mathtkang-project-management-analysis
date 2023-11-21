from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=128, )  # 팀이름
    board_name = models.CharField(max_length=128, )  # 보드이름