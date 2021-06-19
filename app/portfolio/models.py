from django.db import models
from django.contrib.auth import get_user_model

from utils.helpers import make_id

User = get_user_model()


class Portfolio(models.Model):
    PREFIX = 'prt_'

    portfolio_id = models.CharField(max_length=50, unique=True, editable=False)
    reference = models.CharField(null=True, blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    completed = models.DateTimeField(null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)

    class Meta:
        """Meta definition for Portfolio."""

        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'

    def save(self, *args, **kwargs):
        if not self.portfolio_id:
            new_id = make_id()
            self.portfolio_id = self.PREFIX + new_id
            if not self.reference:
                self.reference = new_id
        return super(Portfolio, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.portfolio_id

    def __repr__(self):
        return f'<Portfolio> {self.id} | User: {self.user.email} | Reference: {self.reference}'


class Category(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    archived = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f'<Category> {self.title}'


class Section(models.Model):
    PREFIX = 'sct_'

    section_id = models.CharField(max_length=50, unique=True, editable=False)
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, related_name='sections')
    category = models.ForeignKey(Category, models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    completed = models.DateTimeField(null=True, blank=True, editable=False)
    meta = models.JSONField(null=True, blank=True)
    order = models.FloatField(null=True, blank=True)

    class Meta:
        """Meta definition for Section."""

        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['order']

    @property
    def workitem_count(self):
        return len(self.workitems.all())

    def save(self, *args, **kwargs):
        if not self.section_id:
            new_id = make_id()
            self.section_id = self.PREFIX + new_id
        if not self.order:
            self.order = max([x.order for x in self.portfolio.sections.all()], default=0.0) + 0.1
        return super(Section, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.section_id} {self.category.title}'

    def __repr__(self):
        return f'<Section> {self.section_id} {self.portfolio.portfolio_id}'


class Task(models.Model):
    """Model definition for Task."""

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    duration = models.PositiveSmallIntegerField(help_text='Typical duration of this task')
    completion_days = models.PositiveSmallIntegerField(help_text='Expected days to complete \
                                                       a WorkItem with this task')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    archived = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta definition for Task."""

        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """Unicode representation of Task."""
        return self.title

    def __repr__(self):
        return f'<Task> {self.title}'


class WorkItem(models.Model):
    PREFIX = 'wrk_'

    workitem_id = models.CharField(max_length=50, unique=True, editable=False)
    section = models.ForeignKey(Section, models.DO_NOTHING, related_name='workitems')
    task = models.ForeignKey(Task, models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, models.DO_NOTHING, null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True, editable=False)
    meta = models.JSONField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, models.DO_NOTHING, null=True, blank=True, related_name='assigned_users')
    expected_date = models.DateTimeField(null=True, blank=True)
    order = models.FloatField(null=True, blank=True)

    class Meta:
        """Meta definition for WorkItem."""

        verbose_name = 'Work Item'
        verbose_name_plural = 'Work Items'
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.workitem_id:
            new_id = make_id()
            self.workitem_id = self.PREFIX + new_id
        if not self.order:
            self.order = max([x.order for x in self.section.workitems.all()], default=0.0) + 0.1
        return super(WorkItem, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """Unicode representation of WorkItem."""
        return f'{self.workitem_id} {self.task.title}'

    def __repr__(self):
        return f'<WorkItem> {self.workitem_id} {self.section.section_id} {self.portfolio.portfolio_id}'
