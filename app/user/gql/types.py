from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', )
