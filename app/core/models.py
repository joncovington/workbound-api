import io
import sys
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission
from phonenumber_field.modelfields import PhoneNumberField

from core.managers import CustomUserManager

# to automatically create one to one object
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    firebase_uid = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):

    def upload_image_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/profile_{1}'.format(instance.user.id, filename)

    def upload_thumbnail_path(instance, filename):
        return 'user_{0}/profile_thumb_{1}'.format(instance.user.id, filename)

    def create_thumb(self):
        name = self.image.name
        _image = Image.open(self.image)
        w, h = _image.size
        h = 200
        content_type = Image.MIME[_image.format]
        r = h / _image.size[1]  # ratio
        w = int(_image.size[0] * r)
        imageTemproaryResized = _image.resize((w, h))
        file = io.BytesIO()
        imageTemproaryResized.save(file, _image.format)
        file.seek(0)
        size = sys.getsizeof(file)
        return file, name, content_type, size

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=upload_thumbnail_path,
                                  editable=False,
                                  blank=True,
                                  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.image and self.user:
            file, name, content_type, size = self.create_thumb()
            self.thumbnail = InMemoryUploadedFile(
                file,
                'ImageField',
                name,
                content_type,
                size,
                None
            )
        if not self.image:
            self.thumbnail = None
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def add_view_permissions(sender, instance, created, **kwargs):
    view_permissions = ['Can view Portfolio', 'Can view Section', 'Can view Work Item', 'Can view Category', 'Can view Task', ]
    if created:
        if not instance.is_superuser and not instance.is_staff:
            for perm in view_permissions:
                print('Adding perm: ', perm)
                permission = Permission.objects.get(name=perm)
                instance.user_permissions.add(permission)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
