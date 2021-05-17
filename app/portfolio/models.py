from django.db import models


class Portfolio(models.Model):
    reference = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.reference
