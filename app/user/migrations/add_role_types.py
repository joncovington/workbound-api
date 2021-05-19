from django.db import migrations

def add_role_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    RoleType = apps.get_model('user', 'RoleType')
    RoleType.objects.get_or_create(name='User', level=1.0)
    RoleType.objects.get_or_create(name='Manager', level=9.0)


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_role_types),
    ]
