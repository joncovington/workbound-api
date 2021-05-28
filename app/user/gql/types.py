from django.contrib.auth import get_user_model
from graphene import Int
from graphene_django import DjangoObjectType


User = get_user_model()


class UserType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = User
        exclude = ('password', )
