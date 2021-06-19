# Generated by Django 3.2.3 on 2021-06-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_auto_20210606_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['order'], 'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AlterModelOptions(
            name='workitem',
            options={'ordering': ['order'], 'verbose_name': 'Work Item', 'verbose_name_plural': 'Work Items'},
        ),
        migrations.AlterField(
            model_name='section',
            name='order',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='order',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
