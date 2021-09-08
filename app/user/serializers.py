from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.exceptions import APIException
from firebase_admin import auth

from core.models import Profile
from user.models import Role

from utils.email import send_email


class UserExistsException(APIException):
    status_code = 409
    default_detail = 'User already exists'
    default_code = 'resource_conflict'

    def __init__(self, detail):
        if detail is not None:
            self.detail = {'detail': [force_text(detail)]}
        else:
            self.detail = {"detail": force_text(self.default_detail)}


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['created_at', 'updated_at', 'user']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """Create new user with encrypted password and return it"""
        print('creating user: ', validated_data['email'])
        try:
            firebase_user = auth.create_user(**validated_data)
            firebase_uid = firebase_user.uid

        except auth.EmailAlreadyExistsError:
            print('Firebase user already exists')
            raise serializers.ValidationError('firebase user could not be created')

        if firebase_user:
            print('sending verification link to: ', validated_data['email'])
            link = auth.generate_email_verification_link(validated_data['email'])
            print(link)
            email_body_text = "Thanks for registering your account with Workbound\n" + \
                f"Please verify your email address by visiting this link: {link}"
            email_body_html = (
                "<html>\n"
                "<body>\n"
                "<p>Thanks for registering your account with Workbound<br />"
                f"Please verify your email address by visiting this link: <a href={link}>{link}</a>"
                "</p>"
                "</body>"
                "</html>"
            )
            send_email(validated_data['email'], 'Workbound Email verification link', email_body_text, email_body_html)

        if get_user_model().objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        else:
            user = get_user_model().objects.create_user(**validated_data)

        user.firebase_uid = firebase_uid
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user saving password correctly and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'user', 'category', 'role_type', ]
        read_only_fields = ['id', ]

    def to_representation(self, instance):
        representation = super(RoleSerializer, self).to_representation(instance)
        representation['user'] = UserSerializer(instance=instance.user).data
        representation['category'] = str(instance.category)
        representation['role_type'] = str(instance.role_type)
        return representation
