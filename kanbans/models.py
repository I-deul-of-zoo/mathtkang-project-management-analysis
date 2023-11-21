from django.db import models
from django.contrib.auth import get_user_model
from teams.models import Team
from auths.models import User


class Column(models.Model):
    name = models.CharField(max_length=128, )  # 항목(이름)
    order = models.PositiveIntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.order:
            # order 값이 없을 경우 id 값으로 설정
            max_order = Column.objects.aggregate(models.Max('id'))['id__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)

TAG_CHOICES = (
    (0, 'Not Started'),
    (1, 'In Progress'),
    (2, 'Done'),
)

class Ticket(models.Model):
    order = models.PositiveIntegerField()  # 순서
    title = models.CharField(max_length=128, )  # 제목
    tag = models.IntegerField(choices=TAG_CHOICES, default=0)  # 태그
    work_hours = models.FloatField(default=1.0)  # 작업분량(추정시간)
    due_date = models.DateTimeField()  # 마감시간
    column = models.ForeignKey(Column, on_delete=models.CASCADE)  # 해당 ticket 상위 column
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)  # 해당 ticket 담당자
