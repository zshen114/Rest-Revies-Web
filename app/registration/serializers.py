from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Registration E-mail Address',
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already in use",)]
    )

    @staticmethod
    def send_registration_email(email, code):
        msg = EmailMessage(
            subject='Your Motion Registration',
            body=f'Hello , here is your registration code -->{code}',
            to=[email],
        )
        msg.send()

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User.objects.create_user(
            username=email,
            email=email,
            is_active=False,

        )
        self.send_registration_email(email, new_user.user_profile.code)
        return new_user


class RegistrationValidationSerializer(RegistrationSerializer):
    email = serializers.CharField()
    validation_code = serializers.CharField()
    username = serializers.CharField()
    location = serializers.CharField()
    password = serializers.CharField()
    password_repeat = serializers.CharField()

    def validate_email(self, value):
        try:
            return User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exists!')

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError('username already exists')
        except User.DoesNotExist:
            return value

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def validate(self, attrs):
        user = attrs.get('email')
        if attrs.get('password') != attrs.get('password_repeat'):
            raise serializers.ValidationError({
                'password_repeat': 'passwords do not match'
            })
        if attrs.get('validation_code') != user.user_profile.code or user.is_active:
            raise serializers.ValidationError({
                'code': 'Invalid code or user is already validated!',
            })
        return attrs

    def save(self, validated_data):
        user = validated_data.get('email')
        user.username = validated_data.get('username')
        user.is_active = True
        user.set_password(validated_data.get('password'))
        user.save()
        return user
