from django.contrib.auth import get_user_model
import factory
from core.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('email', )

    email = factory.Iterator(['admin2@workbound.info', 'anotherAdmin@workbound.info'])
    password = factory.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""

        email = kwargs['email']
        password = kwargs['password']
        manager = cls._get_manager(model_class)

        # The default would use ``manager.create(*args, **kwargs)``
        try:
            user = get_user_model().objects.get(email=email)
            return user
        except Exception as e:
            print(e, 'No user exists')
            user = manager.create_superuser(email=email, password=password)

        return user
