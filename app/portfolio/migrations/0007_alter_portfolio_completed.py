# Generated by Django 3.2.3 on 2021-05-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_auto_20210520_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
