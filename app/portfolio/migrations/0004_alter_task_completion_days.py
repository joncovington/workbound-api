# Generated by Django 3.2.3 on 2021-06-06 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_task_completion_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion_days',
            field=models.PositiveSmallIntegerField(default=1, help_text='Expected days to complete                                                        a WorkItem with this task'),
            preserve_default=False,
        ),
    ]