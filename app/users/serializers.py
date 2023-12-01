from rest_framework import serializers
from api.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'location', 'member_since', 'phone', 'bio', 'interests', 'profile_pic']
        read_only_fields = ['id', 'member_since']


class UserNestedSerializer(serializers.ModelSerializer):

    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_profile']
