# Generated by Django 3.2.3 on 2021-05-24 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
