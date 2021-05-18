from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Portfolio(models.Model):
    reference = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self) -> str:
        return self.reference

    def __repr__(self):
        return f'<Portfolio> {self.reference} | User: {self.user.email} | Created: {timezone.localtime(self.created)}'


