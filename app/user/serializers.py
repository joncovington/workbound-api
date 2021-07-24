from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Profile
from user.models import Role


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
        return get_user_model().objects.create_user(**validated_data)

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
