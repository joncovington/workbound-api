import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(User.objects.all()) == 0:
            email = os.getenv("DJANGO_SUPERUSER_EMAIL")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
            print(f"Creating account for {email}")
            admin = User.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
        else:
            print(_("Admin accounts can only be initialized if no Accounts exist"))
