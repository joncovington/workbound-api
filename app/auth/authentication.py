import secrets
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import authentication, status
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
import firebase_admin.auth as auth
from rest_framework.response import Response

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get("Authorization")
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            email = decoded_token["email"]
            uid = decoded_token["uid"]
        except AuthenticationFailed:
            return None

        try:
            # if user doesn't exist, create the user after firebase authentication then map firebase uid
            users = User.objects.filter(email=email)
            if len(users) == 0 and email and uid:
                rand_pass = secrets.token_urlsafe(16)
                user = User.objects.create(
                    email=email, firebase_uid=uid, password=rand_pass
                )
            else:
                user = User.objects.get(email=email)

            if user.firebase_uid is None:
                user.firebase_uid = uid
                user.save()
            return (user, None)

        except ObjectDoesNotExist:
            return None
        except IntegrityError:
            return Response(data={'message': 'This user already exists'}, status=status.HTTP_401_UNAUTHORIZED)
