from django.contrib.auth import get_user_model
from django.db import models

from portfolio.models import Category


class RoleType(models.Model):

    name = models.CharField(max_length=30, unique=True)
    level = models.FloatField()

    def __str__(self) -> str:
        return f'{self.name} | {self.level}'


class Role(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    role_type = models.ForeignKey(RoleType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'category', 'role_type']
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.user.email} | {self.category} | {self.role_type.name}'
