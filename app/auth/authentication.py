from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
import firebase_admin.auth as auth

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get("Authorization")

        try:
            decoded_token = auth.verify_id_token(token)
            email = decoded_token["email"]
        except AuthenticationFailed:
            return None
        except ValueError:
            return None
        except auth.InvalidIdTokenError:
            return None
        try:
            user = User.objects.get(email=email)
            return (user, None)
        except ObjectDoesNotExist:
            return None
