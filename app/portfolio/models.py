from django.db import models
from django.contrib.auth import get_user_model

from utils.helpers import make_id

User = get_user_model()


class Portfolio(models.Model):
    portfolio_id = models.CharField(max_length=50, unique=True, editable=False)
    reference = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    completed = models.DateTimeField(null=True, blank=True, editable=False)
    meta = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.portfolio_id:
            self.portfolio_id = make_id('FOLIO')
        return super(Portfolio, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.portfolio_id

    def __repr__(self):
        return f'<Portfolio> {self.id} | User: {self.user.email} | Reference: {self.reference}'


class SectionCategory(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    archived = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Section Categories'

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f'<Section Category> {self.name}'


class Section(models.Model):
    section_id = models.CharField(max_length=50, unique=True, editable=False)
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, related_name='sections')
    category = models.ForeignKey(SectionCategory, models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    completed = models.DateTimeField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.section_id:
            self.section_id = make_id('SECTION')
        return super(Section, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.section_id} {self.category.name}'

    def __repr__(self):
        return f'<Section> {self.section_id} {self.portfolio.portfolio_id}'
